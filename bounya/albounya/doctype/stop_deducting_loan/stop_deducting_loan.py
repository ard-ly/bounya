# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from frappe.utils import date_diff, month_diff, add_months
from datetime import datetime,timedelta
from frappe.desk.form.utils import add_comment
from frappe.model.document import Document

class StopDeductingLoan(Document):

	def validate(self):
		self.checkdate()

	def on_submit(self):
		self.stop_deducting()
	
	def on_cancel(self):
		self.return_deductions()

	def checkdate(self):
		if frappe.utils.date_diff(str(self.end_date), str(self.start_date)) < 0:
			frappe.throw(_(" Start Date can not be before End Date!"))

	def stop_deducting(self):
			for row in self.stop_deducting_employees:
				total_payment = frappe.db.get_value('Repayment Schedule', row.repayment_schedule, 'total_payment')
				principal_amount = frappe.db.get_value('Repayment Schedule', row.repayment_schedule, 'principal_amount')
				
				# update the stop ducting row in Repayment Schedule.
				frappe.db.sql(f""" UPDATE `tabRepayment Schedule` SET total_payment = '0', balance_loan_amount = balance_loan_amount + '{principal_amount}', custom_row_status = 'Deducting Stop' WHERE name = '{row.repayment_schedule}' """,as_dict=1,)
				cu_idx = frappe.db.get_value('Repayment Schedule', row.repayment_schedule, 'idx')
				
				repayment_schedule= frappe.db.sql(f""" SELECT *  FROM `tabRepayment Schedule` WHERE parent = '{row.loan}' """,as_dict=1,)
				new_idx =len(repayment_schedule)+1
				payment_date = frappe.db.get_value('Repayment Schedule', {'parent': row.loan, 'idx' : len(repayment_schedule) }, ['payment_date'])
				balance_loan_amount = frappe.db.get_value('Repayment Schedule',  {'parent': row.loan, 'idx' : len(repayment_schedule) }, ['balance_loan_amount'])
				next_month = add_months(payment_date,1)
				
				# update all rows in Repayment Schedule.
				next_idx = cu_idx
				for repay in repayment_schedule:
					next_idx += 1
					if next_idx <= len(repayment_schedule):
						frappe.db.sql(f""" UPDATE `tabRepayment Schedule` SET balance_loan_amount = balance_loan_amount +'{total_payment}'  WHERE parent = '{row.loan}' AND idx = '{next_idx}' """,as_dict=1,)
						
				# new Repayment Schedule (last row).
				new_repayment = frappe.new_doc("Repayment Schedule")
				new_repayment.idx = new_idx
				new_repayment.payment_date = next_month
				new_repayment.principal_amount = principal_amount
				new_repayment.interest_amount = 	0.0			
				new_repayment.total_payment = total_payment
				new_repayment.balance_loan_amount = balance_loan_amount
				new_repayment.parent = row.loan
				new_repayment.parentfield = 'repayment_schedule'
				new_repayment.parenttype = 'Loan'
				new_repayment.custom_row_status = "Deducting delay"
				new_repayment.insert(ignore_permissions=True)

				# add comment to the loan.
				loan_name = frappe.get_doc('Loan', row.loan)
				the_date = frappe.db.get_value('Repayment Schedule', row.repayment_schedule, 'payment_date')
				TE = f"<a href='/app/stop-deducting-loan/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"
				loan_name.add_comment("Comment",text=""" loan deducting were stoped for : {the_date} by {TE}.""".format(TE = TE, the_date =the_date ), )
				
	# on cancel.
	def return_deductions(self):
		for row in self.stop_deducting_employees:
			pass					
	# 	loan_name = frappe.get_doc('Loan', d.parent)
	# 	the_date = d.payment_date
	# 	TE = f"<a href='/app/stop-deducting-loan/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"
	# 	loan_name.add_comment("Comment",text=""" Stop Deducting Loan were canceled for : {the_date} by {TE}.""".format(TE = TE, the_date =the_date ), )

	# ajax call.
	@frappe.whitelist()
	def get_employees(self,start_date,end_date):
		# return start_date
		employees={}
		if self.department and self.branch:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE department = '{self.department}' And branch = '{self.branch}' """,as_dict=1,)
			
		elif self.department:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE department = '{self.department}'""",as_dict=1,)
		
		elif self.branch:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE branch = '{self.branch}'""",as_dict=1,)
		
		else:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee`""",as_dict=1,)

		loans_dict = []
		for e in employees:
			loans = frappe.db.sql(f""" SELECT *  FROM `tabLoan` WHERE docstatus = 1 AND applicant = '{e.name}'""",as_dict=1,)
			if loans:
				for l in loans:
					repayment_schedule= frappe.db.sql(f""" SELECT *  FROM `tabRepayment Schedule` WHERE docstatus = 1 AND parent = '{l.name}' """,as_dict=1,)
					for d in repayment_schedule:
						# msgprint("idx: "+str(d.idx))
						# msgprint(str(date_diff(d.payment_date,start_date)))
						# msgprint(str(date_diff(end_date,d.payment_date)))
						# msgprint("----------------------------")
						if date_diff(d.payment_date,start_date) < date_diff(end_date,d.payment_date):
								self.save()
								loans_dict.append([e.name, d.parent,d.name,d.payment_date])
								employees_table = frappe.new_doc("Stop Deducting Employees")
								employees_table.employee = e.name
								employees_table.loan = d.parent
								employees_table.employee_name = e.employee_name
								employees_table.parent = self.doctype_name
								employees_table.parentfield = 'stop_deducting_employees'
								employees_table.parenttype = 'Stop Deducting Loan'
								employees_table.repayment_schedule = d.name
								employees_table.insert(ignore_permissions=True)

		return loans_dict
		