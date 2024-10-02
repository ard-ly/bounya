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
		self.update_available_area_on_submit()
	
	def on_cancel(self):
		self.remove_tower_equipment_table()
		self.update_available_area_on_cancel()
	
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
	
	def update_available_area_on_submit(self):
		if self.equipment_radius:
			if self.equipment_radius > 0:
				tower_doc = frappe.get_doc('Towers', self.tower)
				if tower_doc.available_area:
					if tower_doc.available_area > 0:
						rad_in_m = self.equipment_radius * 0.01
						new_available_area = tower_doc.available_area - rad_in_m
						if new_available_area >= 0:
							frappe.db.sql(f""" UPDATE `tabTowers` SET available_area = {new_available_area} WHERE name = '{self.tower}' """,as_dict=1,)
							# frappe.db.set_value('Towers', self.tower, 'available_area', new_available_area)
						else:
							throw(_("The equipment Radius is more than the tower's available area."))

	
	def remove_tower_equipment_table(self):
		frappe.db.sql(f""" DELETE FROM `tabTowers Equipment table` WHERE equipment_installation = '{self.name}' """)

	def update_available_area_on_cancel(self):
		if self.equipment_radius:
			if self.equipment_radius > 0:
				tower_doc = frappe.get_doc('Towers', self.tower)
				if tower_doc.available_area:
					if tower_doc.available_area > 0:
						rad_in_m = self.equipment_radius * 0.01
						new_available_area = tower_doc.available_area + rad_in_m
						frappe.db.sql(f""" UPDATE `tabTowers` SET available_area = {new_available_area} WHERE name = '{self.tower}' """,as_dict=1,)

						# frappe.db.set_value('Towers', self.tower, 'available_area', new_available_area)

		
