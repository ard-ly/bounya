# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

# import frappe


from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Employee Number"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options":"Employee",
			"width": 100,
		},
		{
			"label": _("Full Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Contract Start"),
			"fieldname": "final_confirmation_date",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Contract End"),
			"fieldname": "contract_end_date",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Note"),
			"fieldname": "custom_contract_no",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Contract Value"),
			"fieldname": "base",
			"fieldtype": "Currency",
			"width": 100,
		},
	]

def get_data(filters=None):
	conditions = get_conditions(filters)
	Employee = frappe.db.sql("""
		SELECT emp.employee, emp.employee_name, emp.final_confirmation_date,
			emp.contract_end_date, ss.base, emp.branch , emp.custom_contract_no
		FROM `tabEmployee` emp
		LEFT JOIN (
			SELECT employee, MAX(from_date) AS max_from_date
			FROM `tabSalary Structure Assignment`
			GROUP BY employee
		) AS latest_ss ON latest_ss.employee = emp.name
		LEFT JOIN `tabSalary Structure Assignment` ss ON
			ss.employee = emp.name AND ss.from_date = latest_ss.max_from_date
		{}
	""".format(conditions), as_dict=True)

	return Employee

def get_conditions(filters):
	conditions = ["ss.docstatus=1" , "emp.custom_contract_type ='Unclassified'" , "emp.status='Active'"]

	if filters.get("company"):
		conditions.append("ss.company='{}'".format(filters.get("company")))

	if filters.get("employee"):
		conditions.append("ss.employee='{}'".format(filters.get("employee")))

	if filters.get("from_date"):
		conditions.append("emp.final_confirmation_date >= '{}'".format(filters.get("from_date")))

	if filters.get("to_date"):
		conditions.append("emp.contract_end_date <= '{}'".format(filters.get("to_date")))

	if filters.get("employee_name"):
		conditions.append("ss.employee_name LIKE '%{}%'".format(filters.get("employee_name")))

	if filters.get("branch"):
		conditions.append("emp.branch='{}'".format(filters.get("branch")))

	return " WHERE " + " AND ".join(conditions)
