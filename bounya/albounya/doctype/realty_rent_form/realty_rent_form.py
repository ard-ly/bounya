# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RealtyRentForm(Document):
	def on_submit(self):
		self.create_lead()


	def create_lead(self):
		new_doc = frappe.new_doc("Lead")
		new_doc.custom_realty_rent_form = 1
		new_doc.custom_realty_rent_form_doctype = self.name
		new_doc.first_name = self.customer
		new_doc.source = "Existing Customer"
		new_doc.customer = self.customer
		if self.customer_branch:
			new_doc.custom_branch = self.customer_branch
		new_doc.insert(ignore_permissions=True)
		self.lead = new_doc.name

		for row in self.realty_rent_table:
			new_tab = frappe.new_doc("Realty Rent Form Table")
			new_tab.parent = new_doc.name
			new_tab.parentfield = "custom_realty_rent_table"
			new_tab.parenttype = "Lead"
			new_tab.realty_type = row.realty_type
			new_tab.realty = row.realty
			new_tab.realty_area = row.realty_area
			new_tab.insert(ignore_permissions=True)
		

		frappe.db.set_value(
                "Realty Rent Form",
                self.name,
                "lead",
                new_doc.name,
            )
		
		users = frappe.db.sql(
				f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE role = 'Tower Management' AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
		for user in users:
				new_doc = frappe.new_doc("Notification Log")
				new_doc.from_user = frappe.session.user
				new_doc.for_user = user.parent
				new_doc.type = "Share"
				new_doc.document_type = "Lead"
				new_doc.document_name =  self.lead
				new_doc.subject = f"""New Lead Created From Realty Rent Form : {self.lead}"""
				new_doc.email_content = "empty@empty.com"
				new_doc.insert(ignore_permissions=True)



