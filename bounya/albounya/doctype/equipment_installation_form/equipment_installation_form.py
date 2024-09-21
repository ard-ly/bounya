# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EquipmentInstallationForm(Document):
	def on_submit(self):
		self.create_lead()

	def create_lead(self):
		new_doc = frappe.new_doc("Lead")
		new_doc.first_name = self.name
		if self.customer:
			new_doc.source = "Existing Customer"
			new_doc.customer = self.customer
		# elif self.user:
		# 	Customer = frappe.db.sql(f"""select name from `tabCustomer` where custom_user = "{self.user}" """)
		# 	if Customer:
		# 		new_doc.source = "Existing Customer"
		# 		new_doc.customer = Customer		
		new_doc.insert(ignore_permissions=True)

		frappe.db.set_value(
                "Equipment Installation Form",
                self.name,
                "lead",
                new_doc.name,
            )