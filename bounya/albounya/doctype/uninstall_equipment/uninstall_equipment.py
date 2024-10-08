# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UninstallEquipment(Document):
	def on_submit(self):
		self.remove_tower_equipment_table()
	
	def on_cancel(self):
		self.add_tower_equipment_table()

	def remove_tower_equipment_table(self):
		if self.equipment_installation:
			tower_doc = frappe.get_doc('Towers', self.tower)
			for row in self.uninstall_equipment_table_tab: 
				frappe.db.sql(f""" UPDATE `tabEquipment Installation Table` SET uninstall_equipment = '{self.name}' WHERE parent = '{self.equipment_installation}' and parenttype = 'Equipment Installation' and equipment_name='{row.equipment_name}' and manufacturer = '{row.manufacturer}' and serial_number = '{row.serial_number}' """,as_dict=1,)
				frappe.db.sql(f""" DELETE FROM `tabTower Equipment Table` WHERE equipment_installation = '{self.equipment_installation}' and equipment_name='{row.equipment_name}' and manufacturer = '{row.manufacturer}' and serial_number = '{row.serial_number}' """)

				equipment_radius = frappe.db.sql(f""" SELECT equipment_radius  FROM `tabEquipment Installation Table` WHERE parent = '{self.equipment_installation}' and parenttype = 'Equipment Installation' and equipment_name='{row.equipment_name}' and manufacturer = '{row.manufacturer}' and serial_number = '{row.serial_number}' """)
				e_r =float(equipment_radius[0][0])
				new_available_area = 0.0
				if e_r > 0:
							rad_in_m = e_r * 0.01
							ava_area = tower_doc.available_area + rad_in_m
							new_available_area += ava_area
				if new_available_area >= 0:
					frappe.db.set_value('Towers', self.tower, 'available_area', new_available_area)


	def add_tower_equipment_table(self):
		if self.equipment_installation:
			ei_doc = frappe.get_doc('Equipment Installation', self.equipment_installation)
			tower_doc = frappe.get_doc('Towers', self.tower)
			for row in ei_doc.equipment_table:
				if row.uninstall_equipment:
					new_doc = frappe.new_doc("Tower Equipment Table")
					new_doc.parent = ei_doc.tower 
					new_doc.parentfield = 'towers_equipment_table'
					new_doc.parenttype = 'Towers'
					new_doc.equipment_installation = ei_doc.name
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

					new_available_area = 0.0
					if tower_doc.available_area > 0:
						if row.equipment_radius:
							if row.equipment_radius > 0:
									rad_in_m = row.equipment_radius * 0.01
									ava_area = tower_doc.available_area - rad_in_m
									new_available_area += ava_area
							if new_available_area >= 0:
								frappe.db.set_value('Towers', self.tower, 'available_area', new_available_area)
					
					frappe.db.sql(f""" UPDATE `tabEquipment Installation Table` SET uninstall_equipment = NULL WHERE parent = '{self.equipment_installation}' and parenttype = 'Equipment Installation' and equipment_name='{row.equipment_name}' and manufacturer = '{row.manufacturer}' and serial_number = '{row.serial_number}' """,as_dict=1,)
