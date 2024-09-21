// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Towers Report"] = {
	"filters": [
		{
			label: __("Tower Name"),
			fieldname: "tower_name",
			fieldtype: "Data",
		},
		
		{
			label: __("Serial Number"),
			fieldname: "serial_number",
			fieldtype: "Data",
		},
		{
			label: __("Tower Type"),
			fieldname: "tower_type",
			fieldtype: "Link",
			options: "Tower Type",
		},
		{
			label: __("Branch"),
			fieldname: "branch",
			fieldtype: "Link",
			options: "Branch",
		},
		{
			label: __("Office"),
			fieldname: "office",
			fieldtype: "Link",
			options: "Office",
		},
	]
};
