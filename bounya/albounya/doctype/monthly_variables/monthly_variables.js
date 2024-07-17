// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
let employee_list = [];

frappe.ui.form.on('Monthly Variables', {
	
	before_load: function (frm) {
		if (frm.is_new()) {
			let monthes = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' , 'October' , 'November' , 'December']
			const today = new Date();
			let month = today.getMonth(); // returns from 0 to 11
			frm.doc.month = monthes[month];
			frm.refresh_fields();
			frm.trigger("month")
	}
	},

	onload: function(frm){
		// get Salary Components from payroll settings.
		frappe.call({
			method :"get_salary_components",
			doc:frm.doc,
			callback:function(r){
				if(r.message){
					employee_list = r.message;
					console.log("components:");
					console.log(employee_list);
				}
			}
		});

		frm.set_query("salary_component", function () {
			return {
			  filters: [
				["Salary Component", 'salary_component', 'in',  employee_list ],
			  ],
			};
		  });

	  
	},

	refresh(frm) {
		// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
				frappe.breadcrumbs.clear();
				
		// Now add breadcrumb for the 'parent' document
				frappe.breadcrumbs.set_custom_breadcrumbs({
						label: cur_frm.doc.doctype, //the name of the field in Doc 2 that points to Doc 1
						route: '/app/' + frappe.scrub(cur_frm.doc.doctype).replace('_', '-'),
						});

				// Finally add the breadcrumb for this document  
				frappe.breadcrumbs.set_custom_breadcrumbs({
						label: cur_frm.doc.name,
						route: '/app/' + frappe.scrub(cur_frm.doc.doctype).replace('_', '-') 
						});

	},

	month(frm) {
		if (frm.doc.month) {

			const d = new Date();
			let year = d.getFullYear();

			let month = frm.doc.month
			var dateString = '' + year + '-' + month + '-' + '24';
			var combined = new Date(dateString);
			
			frm.doc.to_date = moment(combined).format('YYYY-MM-DD');
			let from_date =  frappe.datetime.add_months(combined, -1);
			let from_date_1 = frappe.datetime.add_days(from_date, 1);
			frm.doc.from_date = moment(from_date_1).format('YYYY-MM-DD');
			frm.refresh_fields();
		}
	},

	get_employees(frm) {
		frappe.call({
			method :"get_employees",
			doc:frm.doc,
			args: {},
			callback:function(r){
				if(r.message){
					console.log(r.message);
					frm.refresh_field("monthly_variables_settings");
				}
			}
		});
	},

});

frappe.listview_settings['Monthly Variables'] = {
	refresh: function (listview) {
			// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
		frappe.breadcrumbs.clear();				
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
				label: 'Payroll', //the name of the field in Doc 2 that points to Doc 1
				route: '/app/payroll',
		});
				
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
				label: 'Payroll', //the name of the field in Doc 2 that points to Doc 1
				route: '/app/payroll',
		});
		},
	}
	