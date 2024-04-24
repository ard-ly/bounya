# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyPromotion(Document):
	
	@frappe.whitelist()
	def get_employees(self):
		employees={}
		return str(employees)
