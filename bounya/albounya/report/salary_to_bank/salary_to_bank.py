# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

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
			# "fieldtype": "Link",
			# "options":"Employee",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Full Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Account Number"),
			"fieldname": "bank_account_no",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Net Salary"),
			"fieldname": "net_pay",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("National Number"),
			"fieldname": "custom_national_number",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Month"),
			"fieldname": "month",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Year"),
			"fieldname": "year",
			"fieldtype": "Data",
			"width": 100,
		},
	]

def get_data(filters=None):
	conditions = get_conditions(filters)

	slips = frappe.db.sql("""
				SELECT ss.employee , ss.employee_name, ss.bank_name, ss.bank_account_no , ss.custom__employee_bank_branch , ss.net_pay , emp.custom_national_number
		    	FROM `tabSalary Slip` ss
				LEFT JOIN `tabEmployee` emp ON ss.employee=emp.name
		       	{}
			""".format(conditions), as_dict=True)
	date_obj = frappe.utils.getdate(format(filters.get("to_date")))
	year = date_obj.strftime('%Y')
	print (date_obj)
	month = date_obj.strftime('%m')
	for s in slips:
		s["month"] = month
		s["year"] = year
	return slips

def get_conditions(filters):
	conditions = ["ss.status='Submitted'", "emp.salary_mode='Bank'"]

	if filters.get("company"):
		conditions.append("ss.company='{}'".format(filters.get("company")))

	if filters.get("employee"):
		conditions.append("ss.employee='{}'".format(filters.get("employee")))

	if filters.get("bank"):
		conditions.append("ss.bank_name='{}'".format(filters.get("bank")))

	if filters.get("bank_branch"):
		conditions.append("ss.custom__employee_bank_branch='{}'".format(filters.get("bank_branch")))

	if filters.get("from_date"):
		conditions.append("ss.start_date >= '{}'".format(filters.get("from_date")))

	if filters.get("to_date"):
		conditions.append("ss.end_date <= '{}'".format(filters.get("to_date")))

	if filters.get("employee_name"):
		conditions.append("ss.employee_name LIKE '%{}%'".format(filters.get("employee_name")))

	return " WHERE " + " AND ".join(conditions)
