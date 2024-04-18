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
	def get_employees(self):
		self.checkdate()

		s_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
		e_date  = datetime.strptime(self.end_date, '%Y-%m-%d').date()
		# s_day = str(s_date.day)
		# s_month = str(s_date.month)
		# s_year = str(s_date.year)
		# s_date_combined = ""+s_day+"-"+s_month+"-"+s_year
		# s_date_formated = datetime.strptime(s_date_combined, '%d-%m-%Y').date()
		
		employees={}
		if self.department and self.branch:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE department = '{self.department}' And branch = '{self.branch}' """,as_dict=1,)
			
		elif self.department:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE department = '{self.department}'""",as_dict=1,)
		
		elif self.branch:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE branch = '{self.branch}'""",as_dict=1,)
		
		else:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee`""",as_dict=1,)
		
		if len(employees) > 0:
			for e in employees:
				loans = frappe.db.sql(f""" SELECT *  FROM `tabLoan` WHERE docstatus = 1 AND applicant = '{e.name}'""",as_dict=1,)
				if loans:
					for l in loans:
						repayment_schedule= frappe.db.sql(f"""SELECT *  FROM `tabRepayment Schedule` WHERE docstatus = 1 AND parent = '{l.name}' AND (payment_date BETWEEN '{s_date}' and '{e_date}')""",as_dict=1,)
						for d in repayment_schedule:	   
							self.append(
									"stop_deducting_employees",
									{
										"employee" :e.name,
										"employee_name":e.employee_name,
										"loan":d.parent,
										"repayment_schedule":d.name,
									},
								)						
				else:
					msgprint(_("Employee \""+ e.employee_name +"\" does not have loans."))

		elif len(employees) == 0:
			msgprint(_("There is no employess in this branch and this department."))
		
		return s_date
		
		