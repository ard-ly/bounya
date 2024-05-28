// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Payment loan Report"] = {
	
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
			"default":frappe.datetime.add_days(frappe.datetime.month_start(frappe.query_report.get_filter('month')),23),
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
		},
		{
			"fieldname": "loan_type",
			"label": __("Loan Type"),
			"fieldtype": "Link",
			"width": "200",
			"options": "Loan Type",
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": "100px"
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

	],
	"onload": function (report){ 
		report.page.fields_dict['month'].$input.on('change', function () {
			var cur_year = frappe.datetime.str_to_obj(frappe.datetime.get_today()).getFullYear();
			var cur_month = frappe.query_report.get_filter_value('month')
			var pre_month = frappe.query_report.get_filter_value('month') -1
			var from_d = '' + cur_year + '-' + pre_month + '-' + '25';
			var to_d = '' + cur_year + '-' + cur_month + '-' + '24';
			
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

