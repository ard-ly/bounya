// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Variables Report"] = {
	"filters": [

		{
			label: __("Month"),
			fieldname: "month",
			fieldtype: "Select",
			options:[
				"\n",
				{ "value": 1, "label": __("January") },
				{ "value": 2, "label": __("February") },
				{ "value": 3, "label": __("March") },
				{ "value": 4, "label": __("April") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("August") },
				{ "value": 9, "label": __("September") },
				{ "value": 10, "label": __("October") },
				{ "value": 11, "label": __("November") },
				{ "value": 12, "label": __("December") },
			],
			default: frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		   },
		   {
			label: __("From"),
			fieldname: "from_date",
			fieldtype: "Date",
			default:frappe.datetime.add_days(frappe.datetime.month_start(frappe.query_report.get_filter('month')),-6),
		   },
		   {
			label: __("To"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.month_start(frappe.query_report.get_filter('month')),24),
		   },
		   {
			label: __("Branch"),
			fieldname: "branch",
			fieldtype: "Link",
			options: "Branch",
		   },
		   {
			label: __("Salary Component"),
			fieldname: "salary_component",
			fieldtype: "Link",
			options: "Salary Component",
		   },
		   {
			label: __("Salary Component Type"),
			fieldname: "salary_component_type",
			fieldtype: "Select",
			options: "\nEarning\nDeduction",
		   },
		   {
			label: __("Employee"),
			fieldname: "employee",
			fieldtype: "Link",
			options: "Employee",
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
