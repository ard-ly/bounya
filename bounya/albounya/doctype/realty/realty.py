# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Realty(Document):
	# @frappe.whitelist()
	# def create_asset(source_name, target_doc = None):
	# 	doc = get_mapped_doc("Realty", source_name, {"Realty": {"doctype": "Asset",},"Realty":{"doctype":"Asset","field_map":{"realty_no":"custodian", "location":"city"},},}, target_doc)

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
@frappe.whitelist()
def create_asset(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.custom_asset_type="Realty",
		target.asset_owner="Company",
		target.item_code=source.realty_no,


	doc = frappe.get_doc("Realty", source_name)
	target_doc = get_mapped_doc("Realty", source_name, {
			"Realty": {
				"doctype": "Asset",
				"field_map": {
					"custom_asset_type": "Realty",
					"available_for_use_date": "build_up_date",

				}}
		}, target_doc,
		set_missing_values,
		)
	doc.asset = target_doc.name
	return target_doc