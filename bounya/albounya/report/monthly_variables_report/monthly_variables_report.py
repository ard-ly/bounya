# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	conditions = get_conditions(filters)
	columns =get_columns()
	data = get_data(conditions)
	return columns, data


def get_columns():
	columns = [
		{
		"label": _("Payroll Date"),
		"fieldname": "payroll_date",
		"fieldtype": "Date",
		"width": "100"
		},
		{
		"label": _("Salary Component"),
		"fieldname": "salary_component",
		"fieldtype": "Link",
		"options": "Salary Component",
		
		},
		{
		"label": _("Salary Component Type"),
		"fieldname": "type",
		"fieldtype": "Data",
		"width": "80"
		},
		{
		"label": _("Employee"),
		"fieldname": "employee",
		"fieldtype": "Link",
		"options": "Employee",
		"width": "150"
		},
		{
    	"label": "Amount",
		"fieldname": "amount",
		"fieldtype": "Float",
		},			
		{
    	"label": "Doctype",
		"fieldname": "doctype",
		"fieldtype": "HTML",
		},
	]

	return columns

def get_data(conditions):
	data = frappe.db.sql(f"""
			select payroll_date, salary_component, type, employee, amount, name 
					  from `tabAdditional Salary`
					  where {conditions}
	""", as_dict=True)

	for row in data:
		row.doctype = f"<a target='_blank' onclick='window.open()' href='/app/additional-salary/{row.name}' " \
                              f"title='{row.name}' data-doctype='Additional Salary' data-name='{row.name}'>{row.name}</a>"
				
	return data

def get_conditions(filters):
	conditions = "docstatus=1"
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if from_date and to_date:
		conditions += " AND payroll_date BETWEEN '{0}' AND '{1}'".format(from_date, to_date)
	
	if filters.get("salary_component"):
		conditions += f""" AND salary_component = '{filters.get("salary_component")}'"""

	if filters.get("salary_component_type"):
		conditions += f""" AND type = '{filters.get("salary_component_type")}'"""

	if filters.get("employee"):
		conditions += f""" AND employee = '{filters.get("employee")}'"""

	return conditions