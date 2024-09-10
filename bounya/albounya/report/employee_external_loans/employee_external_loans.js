// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee External Loans"] = {
	"filters": [
		{
			label: __("Employee"),
			fieldname: "employee",
			fieldtype: "Link",
			options: "Employee",
		},
		{
			label: __("Branch"),
			fieldname: "branch",
			fieldtype: "Link",
			options: "Branch",
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: [
				{ "value": "Draft", "label": __("Draft") },
				{ "value": "Paid", "label": __("Paid") },
				{ "value": "Unpaid", "label": __("Unpaid") },
				{ "value": "Cancelled", "label": __("Cancelled") },
			],
			// default: "Unpaid",	
		},
		{
			label: __("Type"),
			fieldname: "type",
			fieldtype: "Link",
			options: "External Loans Type",
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
