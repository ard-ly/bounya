# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from frappe.utils import today
from frappe.model.document import Document

class EquipmentInstallation(Document):

	def validate(self):
		self.validate_installation_date()

	def on_submit(self):
		self.add_tower_equipment_table()
	
	def on_cancel(self):
		self.remove_tower_equipment_table()
	
	def validate_installation_date(self):
		if self.installation_date:
			if self.installation_date > today():
				throw(_("The installation date can not be after today date."))

	def add_tower_equipment_table(self):
		new_doc = frappe.new_doc("Towers Equipment table")
		new_doc.name1 = self.equipment_name
		new_doc.serial_number = self.serial_number
		new_doc.equipment_state = self.equipment_state
		new_doc.parent = self.tower 
		new_doc.parentfield = 'towers_equipment_table'
		new_doc.parenttype = 'Towers'
		new_doc.equipment_installation = self.name
		
		if self.installation_date:
			new_doc.installation_date = self.installation_date
		if self.contract_end_date:
			new_doc.contract_ending_date = self.contract_end_date

		new_doc.insert(ignore_permissions=True)
	
	def remove_tower_equipment_table(self):
		frappe.db.sql(f""" DELETE FROM `tabTowers Equipment table` WHERE equipment_installation = '{self.name}' """)

		
