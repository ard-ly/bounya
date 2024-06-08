// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt
let employee_list = [];

frappe.ui.form.on('Monthly Variables', {
	
	setup: function (frm) {
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
					// console.log("aaaaaaaaaaaaaaaaaaaaaaaaa");
					// console.log(r.message);
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

	month(frm) {
		if (frm.doc.month) {

			const d = new Date();
			let year = d.getFullYear();

			let month = frm.doc.month
			var dateString = '' + year + '-' + month + '-' + '24';
			var combined = new Date(dateString);
			
			frm.doc.to_date = new Date(dateString);
			let from_date =  frappe.datetime.add_months(combined, -1);
			frm.doc.from_date = new Date(from_date);
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
