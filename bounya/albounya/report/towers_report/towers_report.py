# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

# import frappe


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
            "label": _("Tower Name"),
            "fieldname": "tower_name",
            "fieldtype": "Data",
        },
		{
            "label": _("Serial Number"),
            "fieldname": "serial_number",
            "fieldtype": "Data",
        },
        {
            "label": _("Tower Type"),
            "fieldname": "tower_type",
            "fieldtype": "Link",
            "options": "Tower Type",
        },
		{
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
        },
		{
            "label": _("Office"),
            "fieldname": "office",
            "fieldtype": "Link",
            "options": "Office",
        },
		{
            "label": _("Asset"),
            "fieldname": "asset",
            "fieldtype": "Link",
            "options": "Asset",
        },
		{
            "label": _("Tower Weigh"),
            "fieldname": "tower_weigh",
            "fieldtype": "Float",
        },
		{
            "label": _("Tower Height"),
            "fieldname": "tower_height",
            "fieldtype": "Float",
        },
		{
            "label": _("Age Of Tower"),
            "fieldname": "age_of_tower",
            "fieldtype": "Float",
        },
		{
            "label": _("Number Of Equipments"),
            "fieldname": "number_of_equipments",
            "fieldtype": "Int",
        },
		{
            "label": _("Required height For Installation"),
            "fieldname": "required_height_for_installation",
            "fieldtype": "Float",
        },
		{
            "label": _("Allowable Equipment Weight"),
            "fieldname": "allowable_equipment_weight",
            "fieldtype": "Float",
        },
	
	]
	return columns

def get_data(conditions):
	data = frappe.db.sql(f"""SELECT tower_name,serial_number,tower_type,branch,office,asset,tower_weigh,tower_height,age_of_tower,number_of_equipments,required_height_for_installation,allowable_equipment_weight FROM `tabTowers` {conditions}""", as_dict=True)
	return data
	
def get_conditions(filters):
	conditions ="WHERE docstatus=1"
	
	tower_name = filters.get("tower_name")
	serial_number = filters.get("serial_number")
	tower_type = filters.get("tower_type")
	branch = filters.get("branch")
	office = filters.get("office")
	
	if tower_name:
		conditions += " AND tower_name = '{0}' ".format(tower_name)
	if serial_number:
		conditions += " AND serial_number = '{0}' ".format(serial_number)
	if tower_type:
		conditions += " AND tower_type = '{0}' ".format(tower_type)
	if branch:
		conditions += " AND branch = '{0}' ".format(branch)
	if office:
		conditions += " AND office = '{0}' ".format(office)
	
	print(conditions)
	return conditions
