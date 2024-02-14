// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Statement of deductions"] = {
	"filters": [
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			reqd: 1,
			options: [
				{ "value": 1, "label": __("Jan") },
				{ "value": 2, "label": __("Feb") },
				{ "value": 3, "label": __("Mar") },
				{ "value": 4, "label": __("Apr") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("Aug") },
				{ "value": 9, "label": __("Sep") },
				{ "value": 10, "label": __("Oct") },
				{ "value": 11, "label": __("Nov") },
				{ "value": 12, "label": __("Dec") },
			],
			default: frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		},		{
			fieldname:"year",
			label: __("Year"),
			fieldtype: "Select",
			reqd: 1
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": "100px"
		},
		{
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"label": __("Currency"),
			"default": erpnext.get_currency(frappe.defaults.get_default("Company")),
			"width": "50px"
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "100px"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width": "100px",
			"reqd": 1
		},
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default": "Submitted",
			"width": "100px"
		},
		{
			"fieldname": "component",
			"label": __("Salary Component"),
			"fieldtype": "MultiSelectList",
			"width": "200",
			"get_data": function(txt) {
				return frappe.db.get_link_options("Salary Component", txt);
			 }
		},
		{
			"fieldname":"report_type",
			"label":__("Reprt Type"),
			"fieldtype":"Select",
			"options":["Net Pay", "Select Component", "Lone"],
			"default": "Select Component",
			"width": "100px"
		},
		{
			"fieldname": "summetion_component",
			"label": __("Summetion Of Component"),
			"fieldtype": "MultiSelectList",
			"width": "200",
			"get_data": function(txt) {
				return frappe.db.get_link_options("Salary Component", txt);
			 }
		},
		{
			"fieldname":"header",
			"label": __("Print Hedder"),
			"fieldtype": "Data",
			"width": "100px"
		},
	],
	onload: function() {
		return  frappe.call({
			method: "hrms.payroll.report.provident_fund_deductions.provident_fund_deductions.get_years",
			callback: function(r) {
				var year_filter = frappe.query_report.get_filter('year');
				year_filter.df.options = r.message;
				year_filter.df.default = r.message.split("\n")[0];
				year_filter.refresh();
				year_filter.set_input(year_filter.df.default);
			}
		});
	}
}


