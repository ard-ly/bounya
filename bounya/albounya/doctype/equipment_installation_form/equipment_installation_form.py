# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EquipmentInstallationForm(Document):
	def validate(self):
		self.send_notification_to_Tower_management()

	def on_submit(self):
		self.create_lead()

	
	def send_notification_to_Tower_management(self):
		if self. docstatus == 0:
			users = frappe.db.sql(
				f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE role = 'Tower Management' AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
			for user in users:
				new_doc = frappe.new_doc("Notification Log")
				new_doc.from_user = frappe.session.user
				new_doc.for_user = user.parent
				new_doc.type = "Share"
				new_doc.document_type = "Equipment Installation Form"
				new_doc.document_name = self.name
				new_doc.subject = f"""New Equipment Installation Form Created: {self.name}, by: {self.user}"""
				new_doc.email_content = "empty@empty.com"
				new_doc.insert(ignore_permissions=True)
	

	def create_lead(self):
		new_doc = frappe.new_doc("Lead")
		new_doc.custom_equipment_installation_form = 1
		new_doc.custom_equipment_installation_form_doctype = self.name
		new_doc.first_name = self.customer
		new_doc.source = "Existing Customer"
		new_doc.customer = self.customer
		new_doc.insert(ignore_permissions=True)

		frappe.db.set_value(
                "Equipment Installation Form",
                self.name,
                "lead",
                new_doc.name,
            )
		
		users = frappe.db.sql(
				f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'General Management' or role = 'Commercial Management') AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
		for user in users:
				new_doc = frappe.new_doc("Notification Log")
				new_doc.from_user = frappe.session.user
				new_doc.for_user = user.parent
				new_doc.type = "Share"
				new_doc.document_type = "Lead"
				new_doc.document_name =  new_doc.name
				new_doc.subject = f"""New Lead Created From Equipment Installation Form : {new_doc.name}"""
				new_doc.email_content = "empty@empty.com"
				new_doc.insert(ignore_permissions=True)