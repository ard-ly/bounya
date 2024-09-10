// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Continuing employee contracts report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
		},
		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "employee_name",
			"label": __("Employee Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",

		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",

		},
		{
			"fieldname": "letter_head",
			"label": __("Letter Head"),
			"fieldtype": "Link",
			"options": "Letter Head"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"hidden": 1
		},
	]
};
