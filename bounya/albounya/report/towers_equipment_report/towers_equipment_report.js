// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Towers Equipment Report"] = {
	"filters": [
		{
			label: __("Tower"),
			fieldname: "tower",
			fieldtype: "Link",
			options: "Towers",
		},

		{
			label: __("Equipment Name"),
			fieldname: "equipment_name",
			fieldtype: "Data",
		},

		{
			label: __("Serial Number"),
			fieldname: "serial_number",
			fieldtype: "Data",
		},
		
		{
			label: __("Equipment State"),
			fieldname: "equipment_state",
			fieldtype: "Select",
			options: [
				{ "value": "Replacement", "label": __("Replacement") },
				{ "value": "Renewing", "label": __("Renewing") },
				{ "value": "First Installation", "label": __("First Installation") },
				{ "value": "Expired", "label": __("Expired") },
			],
		},
		

	]
};
