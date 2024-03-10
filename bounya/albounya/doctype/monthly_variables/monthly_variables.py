# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyVariables(Document):
	
	def validate(self):
		self.validate_employess()
	
	def on_submit(self):
		self.create_additional_salary()
	
	@frappe.whitelist()
	def get_salary_components(self):
		components = []
		component_list = frappe.db.get_list('Salary Component Settings', fields=['salary_component'],)

		for c in component_list:
			components.append(str(c.salary_component))
		# frappe.msgprint(str(components))
		return components
	
	def validate_employess(self):
		pass

	def create_additional_salary(self):
		pass
