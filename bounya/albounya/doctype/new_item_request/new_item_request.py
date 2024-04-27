# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NewItemRequest(Document):
	def validate(self):
		if frappe.db.exists("Item", self.item_name):
			self.status = "Duplicated"

	@frappe.whitelist()
	def create_item(
		self, item_name, item_category, expense_account, income_account, description=""
	):
		created = False
		if self.default_expense_account and self.default_income_account:
				# create a new document
				item_doc = frappe.get_doc(
					{
						"doctype": "Item",
						"item_code": item_name,
						"item_name": item_name,
						"item_group": item_category,
						"description": description,
						
					}
				)
				item_doc.append("item_defaults", {
							"expense_account": expense_account,
							"income_account": income_account,
						},)
				created = True
				item_doc.insert()

				frappe.db.commit()
		
		return created
