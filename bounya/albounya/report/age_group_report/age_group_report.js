// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Age Group Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"hide": 1
		},
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
				{ "value": "Active", "label": __("Active") },
				{ "value": "Inactive", "label": __("Inactive") },
				{ "value": "Suspended", "label": __("Suspended") },
				{ "value": "Left", "label": __("Left") },
			],
			// default: "Active",	
		},
		{
			label: __("Designation"),
			fieldname: "designation",
			fieldtype: "Link",
			options: "Designation",
		}, 
		{
			label: __("Department"),
			fieldname: "department",
			fieldtype: "Link",
			options: "Department",
		},
		{
			label: __("Designation Type"),
			fieldname: "designation_type",
			fieldtype: "Link",
			options: "Designation Type",
		},
		{
			label: __("Contract Type"),
			fieldname: "contract_type ",
			fieldtype: "Select",
			options: [
				{ "value": "Active", "label": __("تكليف") },
				{ "value": "Inactive", "label": __("غير محدد المدة") },
				{ "value": "Suspended", "label": __("محدد المدة") },
			],
		},
	]
};
