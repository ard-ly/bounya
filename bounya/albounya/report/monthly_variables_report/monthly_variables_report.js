// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

// const d = new Date();
// var cur_year = d.getFullYear();
// var pre_month = d.getMonth() ;
// cur_month = pre_month +1
// var to_d = '' + cur_year + '-' + cur_month + '-' + '25';
// var from_d = '' + cur_year + '-' + pre_month + '-' + '25';
// console.log(new Date(from_d));
// console.log(new Date(to_d));

frappe.query_reports["Monthly Variables Report"] = {
	"filters": [

		{
			label: __("Month"),
			fieldname: "month",
			fieldtype: "Select",
			options: "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
		   },
		   {
			label: __("From"),
			fieldname: "from_date",
			fieldtype: "Date",
		   },
		   {
			label: __("To"),
			fieldname: "to_date",
			fieldtype: "Date",
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
		  
	]
};
