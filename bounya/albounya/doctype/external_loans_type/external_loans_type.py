# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

class ExternalLoansType(Document):
	def validate(self):
		self.update_disable_value()

	def update_disable_value(self):
		eea_list = frappe.get_list("Employee External Loans", filters={'type':self.external_advance_name})
		print(eea_list)

		try:
			for row in eea_list:
				frappe.db.set_value("Employee External Loans",row.name, "payment_disabled", self.disable)
		
		except Exception as e:
			frappe.msgprint(_("A problem in updating Employee External Loans!"))