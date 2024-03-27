# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
import json
from frappe import _, msgprint,throw
from datetime import datetime
from frappe.model.document import Document

class MonthlyVariables(Document):
	
	def validate(self):
		self.validate_employess()
	
	def on_submit(self):
		self.create_additional_salary()
	
	def on_cancel(self):
		self.cancel_additional_salary()
	
	@frappe.whitelist()
	def get_salary_components(self):
		components = []
		component_list = frappe.db.get_all('Salary Component Settings', fields=['salary_component'],)

		for c in component_list:
			components.append(str(c.salary_component))
		# frappe.msgprint(str(components))
		return components
	
	def validate_employess(self):
		for e in self.monthly_variables_settings:
			additional_salary= frappe.db.sql(
            f""" SELECT *  FROM `tabAdditional Salary` WHERE employee = '{e.employee}' AND salary_component = '{self.salary_component}' AND docstatus = 1 """,as_dict=1,)
			# msgprint(str(additional_salary))

			from_date = datetime.strptime(str(self.from_date), '%Y-%m-%d').date()
			to_date = datetime.strptime(str(self.to_date) , '%Y-%m-%d').date()

			for a in additional_salary:
				if from_date <= a.payroll_date <= to_date:
					# msgprint(str(a.name))
					additional_link = f"<a href='/app/additional-salary/{a.name}' style='color: var(--text-on-blue)'>{a.name}</a>"
					throw(_("Employee " + e.employee + " already has an additional salary " + additional_link +" for this component with the amount " + str (a.amount) + "$"))

	def create_additional_salary(self):
		for e in self.monthly_variables_settings:
			try:
				additional = frappe.new_doc("Additional Salary")
				additional.employee = e.employee
				additional.payroll_date = self.from_date
				additional.salary_component = self.salary_component
				additional.amount = e.amount
				additional.custom_monthly_variables = self.name
				additional.save()

				# add comment to the Additional Salary.
				TE = f"<a href='/app/monthly-variables/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"
				additional.add_comment("Comment",text=""" This Additional Salary was created by Monthly Variable {TE}.""".format(TE = TE), )
				
				additional.submit()
				frappe.db.commit()
				additional_link = f"<a href='/app/additional-salary/{additional.name}' style='color: var(--text-on-blue)'>{additional.name}</a>"
				# msgprint(additional_link + " is created.")


			except Exception as e:
				frappe.log_error("Error while creating Additional Salary for", str(e.employee))
				return

	def cancel_additional_salary(self):
			additional_salary_list= frappe.db.sql(
            f""" SELECT *  FROM `tabAdditional Salary` WHERE custom_monthly_variables = '{self.name}'  AND docstatus = 1 """,as_dict=1,)

			for additional in additional_salary_list:
				# add comment to the Additional Salary.
				TE = f"<a href='/app/monthly-variables/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"
				additional.add_comment("Comment",text=""" This Additional Salary was canceled by Monthly Variable {TE}.""".format(TE = TE), )
				additional.cancel()
				frappe.db.commit()