# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from frappe.model.document import Document

class SalesInvoiceDiscountPercentage(Document):
	def validate(self):
		self.validate_percent()

	def validate_percent(self):
		# msgprint("test")
		for row in self.discount_percentage:
			if row.discount_percent > 5:
				throw(_("Discount percentage should be less or equal to %5"))
				return