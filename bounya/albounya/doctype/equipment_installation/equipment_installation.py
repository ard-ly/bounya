# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from frappe.utils import today
from frappe.model.document import Document

class EquipmentInstallation(Document):

	# def validate(self):
	# 	self.validate_installation_date()

	def on_submit(self):
		self.add_tower_equipment_table()
		self.update_available_area_on_submit()
	
	def on_cancel(self):
		self.remove_tower_equipment_table()
		self.update_available_area_on_cancel()

	def add_tower_equipment_table(self):
		for row in self.equipment_table:
			new_doc = frappe.new_doc("Tower Equipment Table")
			new_doc.parent = self.tower 
			new_doc.parentfield = 'towers_equipment_table'
			new_doc.parenttype = 'Towers'
			new_doc.equipment_installation = self.name
			new_doc.equipment_name = row.equipment_name
			new_doc.manufacturer = row.manufacturer
			new_doc.serial_number = row.serial_number
			new_doc.equipment_state = row.equipment_state

			if row.equipment_radius:
				new_doc.equipment_radius = row.equipment_radius
			if row.equipment_height:
				new_doc.equipment_height = row.equipment_height
			if row.equipment_weigh:
				new_doc.equipment_weigh = row.equipment_weigh
			if row.equipment_direction_tab:
				new_doc.equipment_direction_tab = row.equipment_direction_tab
			if row.direction_degrees:
				new_doc.direction_degrees = row.direction_degrees
			if row.installation_date:
				new_doc.installation_date = row.installation_date
			new_doc.insert(ignore_permissions=True)
	
	def update_available_area_on_submit(self):
		new_available_area = 0.0
		tower_doc = frappe.get_doc('Towers', self.tower)
		if tower_doc.available_area > 0:
			for row in self.equipment_table:
				if row.equipment_radius:
					if row.equipment_radius > 0:
						rad_in_m = row.equipment_radius * 0.01
						ava_area = tower_doc.available_area - rad_in_m
						new_available_area += ava_area
		if new_available_area >= 0:
			frappe.db.set_value('Towers', self.tower, 'available_area', new_available_area)
			print(new_available_area)
		else:
			throw(_("The equipment Radius is more than the tower's available area."))

	
	def remove_tower_equipment_table(self):
		frappe.db.sql(f""" DELETE FROM `tabTower Equipment Table` WHERE equipment_installation = '{self.name}' """)

	def update_available_area_on_cancel(self):
		new_available_area = 0.0
		tower_doc = frappe.get_doc('Towers', self.tower)
		if tower_doc.available_area > 0:
			for row in self.equipment_table:
				if row.equipment_radius:
					if row.equipment_radius > 0:
						rad_in_m = row.equipment_radius * 0.01
						ava_area = tower_doc.available_area + rad_in_m
						new_available_area += ava_area
		if new_available_area >= 0:
			frappe.db.set_value('Towers', self.tower, 'available_area', new_available_area)
			print(new_available_area)
		
		
