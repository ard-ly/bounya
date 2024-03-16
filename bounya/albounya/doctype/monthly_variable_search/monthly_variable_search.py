# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from frappe.utils import date_diff, month_diff, add_months
from datetime import datetime,timedelta
from frappe.model.document import Document

class MonthlyVariableSearch(Document):
	@frappe.whitelist()
	def get_employees(self,from_date,to_date):
		old_settings = frappe.db.sql(f""" DELETE FROM `tabMonthly Variables Settings` WHERE parent = 'Monthly Variable Search' """,as_dict=1,)
		frappe.db.commit()
		additional =  frappe.db.sql(f""" SELECT *  FROM `tabAdditional Salary` WHERE docstatus = 1 AND salary_component = '{self.salary_component}'  """,as_dict=1,)
		
		self.save()
		for row in additional:
			if date_diff(row.payroll_date,from_date) < date_diff(to_date,row.payroll_date):
				
				Settings = frappe.new_doc("Monthly Variables Settings")
				Settings.employee = row.employee
				Settings.amount = row.amount
				Settings.parent = 'Monthly Variable Search'
				Settings.parentfield = 'monthly_variables_settings'
				Settings.parenttype = 'Monthly Variable Search'
				Settings.save()
				frappe.db.commit()

		return additional
			
