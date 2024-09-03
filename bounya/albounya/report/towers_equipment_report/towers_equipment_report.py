# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	conditions = get_conditions(filters)
	columns, data =  get_columns(), get_data(conditions)
	return columns, data

def get_columns():
	columns = [
        {
            "label": _("Tower"),
            "fieldname": "tower",
            "fieldtype": "Link",
            "options": "Towers",
        },
		{
            "label": _("Equipment Name"),
            "fieldname": "equipment_name",
            "fieldtype": "Data",
        },
		{
            "label": _("Serial Number"),
            "fieldname": "serial_number",
            "fieldtype": "Data",
        },
		{
            "label": _("Equipment State"),
            "fieldname": "equipment_state",
            "fieldtype": "Data",
        },
		{
            "label": _("Contract End Date"),
            "fieldname": "contract_end_date",
            "fieldtype": "Date",
        },
		{
            "label": _("Installed"),
            "fieldname": "installed",
            "fieldtype": "Check",
        },
		{
            "label": _("Installation Date"),
            "fieldname": "installation_date",
            "fieldtype": "Date",
        },
	]
	return columns

def get_data(conditions):
	data = frappe.db.sql(f"""SELECT tower,equipment_name,serial_number,equipment_state,contract_end_date,installed,installation_date FROM `tabEquipment Installation` {conditions}""", as_dict=True)
	return data
	
def get_conditions(filters):
	conditions ="WHERE docstatus=1"
	tower = filters.get("tower")
	equipment_name = filters.get("equipment_name")
	serial_number = filters.get("serial_number")
	equipment_state = filters.get("equipment_state")
	
	if tower:
		conditions += " AND tower = '{0}' ".format(tower)
	if equipment_name:
		conditions += " AND equipment_name = '{0}' ".format(equipment_name)
	if serial_number:
		conditions += " AND serial_number = '{0}' ".format(serial_number)
	if equipment_state:
		conditions += " AND equipment_state = '{0}' ".format(equipment_state)
	# if installed:
	# 	conditions += " AND installed = '{0}' ".format(installed)
	
	print(conditions)
	return conditions
