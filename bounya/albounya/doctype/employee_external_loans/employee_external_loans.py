# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

class EmployeeExternalLoans(Document):

	def validate(self):
		self.validate_external_advance()
	
	def on_cancel(self):
		self.cancel_external_advance()
	
	# def on_update(self):
	# 	self.update_external_advance()

	def validate_external_advance(self):
		if self.monthly_repayment_amount > self.advance_amount:
			throw(_("The Monthly Repayment Amount must be smaller than the Advance Amount."))

	def cancel_external_advance(self):
		frappe.db.set_value("Employee External Loans",self.name, "status", 'Cancelled')

	# def update_external_advance(self):
	# 	if self.docstatus != 2:
	# 		if self.docstatus != 0:
	# 				if self.remaining_amount == 0:
	# 					frappe.db.set_value("Employee External Loans",self.name, "status", 'Paid')