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
		# {
		# 	"label": _("Branch"),
		# 	"fieldname": "branch",
		# 	"fieldtype": "Data",
		# 	"width": 100,
		# },
		{
			"label": _("Net Salary"),
			"fieldname": "net_pay",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("Loan Type"),
			"fieldname": "loan_type",
			"fieldtype": "Link",
			"options": "Loan Type",
			"width": 200,
		},
		{
			"label": _("Loan Amount"),
			"fieldname": "loan_amount",
			"fieldtype": "Currency",
			"options": "Loan Type",
			"width": 200,
		}, 
		{
			"label": _("Total Principal Paid"),
			"fieldname": "total_principal_paid",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("Total Principal Amount"),
			"fieldname": "total_principal_amount",
			"fieldtype": "Currency",
			"width": 200,
		},
 
		{
			"label": _("Salary Slip"),
			"fieldname": "n",
			"fieldtype": "Link",
			"options": "Salary Slip" ,
			"width": 200,
		},
 
	 	]

def get_data(filters=None):
	conditions = get_conditions(filters)

	slips = frappe.db.sql("""
				SELECT ss.name n, ss.start_date start_date , ss.end_date end_date , ss.*, sl.*  , ss.total_principal_amount  total_principal_amount, l.*    FROM `tabSalary Slip` ss
					INNER JOIN  `tabSalary Slip Loan` sl
					on sl.parent = ss.name
					INNER JOIN `tabLoan` l
					on sl.loan = l.name
					   """.format(conditions), as_dict=True)

	return slips

def get_conditions(filters):
	conditions = ["ss.status='Submitted'"]

	if filters.get("company"):
		conditions.append("ss.company='{}'".format(filters.get("company")))

	if filters.get("employee"):
		conditions.append("ss.employee='{}'".format(filters.get("employee")))


	if filters.get("from_date"):
		conditions.append("ss.start_date >= '{}'".format(filters.get("from_date")))

	if filters.get("to_date"):
		conditions.append("ss.end_date <= '{}'".format(filters.get("to_date")))

	# if filters.get("employee_name"):
	# 	conditions.append("ss.employee_name LIKE '%{}%'".format(filters.get("employee_name")))

	if filters.get("branch"):
		conditions.append("ss.branch='{}'".format(filters.get("branch")))

	return " WHERE " + " AND ".join(conditions)
