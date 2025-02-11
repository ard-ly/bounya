// Copyright (c) 2025, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Promotion Report"] = {
	"filters": [
		{
			label: __("Employee"),
			fieldname: "employee",
			fieldtype: "Link",
			options: "Employee",
		}
	]
};