// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary To Bank"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "employee_name",
			"label": __("Employee Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end()

		},
		{
			"fieldname": "bank",
			"label": __("Bank"),
			"fieldtype": "Link",
			"options": "Employee Bank"
		},
		{
			"fieldname": "bank_branch",
			"label": __("Bank Branch"),
			"fieldtype": "Link",
			"options": "Bank Branch",
			"get_query": function() {
				let bank = frappe.query_report.get_filter_value("bank")
				return {
					query: "bounya.api.fetch_bank_branch_list",
					filters: {
					  bank_name: bank,
					},
				  };
			}
		},
		{
			"fieldname": "letter_head",
			"label": __("Letter Head"),
			"fieldtype": "Link",
			"options": "Letter Head"
		},
		{
			"fieldname": "total_amount",
			"fieldtype": "Data",
			"hidden": 1
		},
		{
			"fieldname": "total_in_words",
			"fieldtype": "Data",
			"hidden": 1
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		$("input[data-fieldname='inst_num']").css({"font-size":"12px", "background-color":"#6c7680", "color":"#fff"});
		value = default_formatter(value, row, column, data);
		total_net_pay = frappe.query_report.data[frappe.query_report.data.length -1].net_pay || 0;
		frappe.query_report.set_filter_value('total_amount', total_net_pay.toFixed(2));
		
		frappe.call({
            method: "bounya.api.money_in_words",
            args: {
                "number": total_net_pay.toFixed(2)
            },
            callback: function (r) {
                if (r.message){
                    frappe.query_report.set_filter_value('total_in_words', r.message)
                }
            }
        })
	
		return value;
	},
};
