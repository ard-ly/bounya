# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from frappe.utils import date_diff, month_diff, add_months
from datetime import datetime,timedelta
from frappe.desk.form.utils import add_comment
from frappe.model.document import Document

class StopDeductingLoan(Document):

	def on_submit(self):
		self.checkdate()
		self.stop_deducting()
	
	def on_cancel(self):
		self.return_deductions()

	def checkdate(self):
		if frappe.utils.date_diff(str(self.end_date), str(self.start_date)) < 0:
			frappe.throw(_(" Start Date can not be before End Date!"))

	def stop_deducting(self):
			repayment_schedule= frappe.db.sql(f""" SELECT *  FROM `tabRepayment Schedule` WHERE docstatus = 1 """,as_dict=1,)

			count = 0
			for d in repayment_schedule:
				# check if d.payment_date is between self.start_date and self.end_date
				# s = datetime.strptime(self.start_date, '%Y-%m-%d').date()
				# e = datetime.strptime(self.end_date , '%Y-%m-%d').date()
				# if s <= d.payment_date <= e:
				if date_diff(d.payment_date,self.start_date) < date_diff(self.end_date,d.payment_date):
					amount = d.total_payment
					for n in repayment_schedule:
						if n.parent == d.parent:
							if (n.idx - d.idx) == 1:
								frappe.db.sql(f""" UPDATE `tabRepayment Schedule` SET total_payment = '0', balance_loan_amount = balance_loan_amount + '{d.principal_amount}' WHERE parent = '{d.parent}'AND idx = '{d.idx}' """,as_dict=1,)
								frappe.db.sql(f""" UPDATE `tabRepayment Schedule` SET total_payment = total_payment + '{amount}' WHERE parent = '{d.parent}'AND idx = '{n.idx}' """,as_dict=1,)
								count += 1

								loan_name = frappe.get_doc('Loan', d.parent)
								the_date = d.payment_date
								TE = f"<a href='/app/stop-deducting-loan/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"

								loan_name.add_comment("Comment",text=""" loan deducting were stoped for : {the_date} by {TE}.""".format(TE = TE, the_date =the_date ), )
								
			msgprint(_("Deducting were stoped for " + str(count))+" loans.")

	# on cancel.
	def return_deductions(self):
			repayment_schedule= frappe.db.sql(f""" SELECT *  FROM `tabRepayment Schedule` WHERE docstatus = 1 """,as_dict=1,)

			for d in repayment_schedule:
				# check if d.payment_date is between self.start_date and self.end_date
				# if self.start_date <= d.payment_date <= self.end_date :
				if date_diff(d.payment_date,self.start_date) < date_diff(self.end_date,d.payment_date):
					total = d.principal_amount + d.interest_amount

					if d.total_payment == 0:
						d.total_payment = total
						for n in repayment_schedule:
							if n.parent == d.parent:
								if (n.idx - d.idx) == 1:
									frappe.db.sql(f""" UPDATE `tabRepayment Schedule` SET total_payment =  {total}, balance_loan_amount = balance_loan_amount - '{total}' WHERE parent = '{d.parent}'AND idx = '{d.idx}' """,as_dict=1,)
									frappe.db.sql(f""" UPDATE `tabRepayment Schedule` SET total_payment = total_payment - '{total}' WHERE parent = '{d.parent}'AND idx = '{n.idx}' """,as_dict=1,)
								
								
									loan_name = frappe.get_doc('Loan', d.parent)
									the_date = d.payment_date
									TE = f"<a href='/app/stop-deducting-loan/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"

									loan_name.add_comment("Comment",text=""" Stop Deducting Loan were canceled for : {the_date} by {TE}.""".format(TE = TE, the_date =the_date ), )

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
						if date_diff(d.payment_date,start_date) < date_diff(end_date,d.payment_date):
							loans_dict.append([e.name, d.parent,d.name,d.payment_date])
							self.save()
							employees_table = frappe.new_doc("Stop Deducting Employees")
							employees_table.employee = e.name
							employees_table.employee_name = e.employee_name
							employees_table.parent = self.doctype_name
							employees_table.parentfield = 'stop_deducting_employees'
							employees_table.parenttype = 'Stop Deducting Loan'
							employees_table.loan = d.parent
							employees_table.repayment_schedule = d.name
							# employees_table.save()
							employees_table.insert(ignore_permissions=True)

		return loans_dict
		