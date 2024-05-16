// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Statement of deductions"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.month_start(frappe.query_report.get_filter('month')),-6),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default":frappe.datetime.add_days(frappe.datetime.month_start(frappe.query_report.get_filter('month')),24),
			"reqd": 1,
			"width": "100px"
		},
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
	"onload": function (report){ 
		report.page.fields_dict['month'].$input.on('change', function () {
			var cur_year = frappe.datetime.str_to_obj(frappe.datetime.get_today()).getFullYear();
			var cur_month = frappe.query_report.get_filter_value('month')
			var pre_month = frappe.query_report.get_filter_value('month') -1
			var from_d = '' + cur_year + '-' + pre_month + '-' + '25';
			var to_d = '' + cur_year + '-' + cur_month + '-' + '25';
			
			frappe.query_report.set_filter_value('to_date', new Date(to_d));
			frappe.query_report.set_filter_value('from_date', new Date(from_d));			
			report.refresh();
		});

		report.page.fields_dict['from_date'].$input.on('change', function () {
			report.refresh();
		});

		report.page.fields_dict['to_date'].$input.on('change', function () {
			report.refresh();
		});
	},
}


