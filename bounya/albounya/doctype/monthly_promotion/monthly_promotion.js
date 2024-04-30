// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Promotion', {
	
	setup: function (frm) {
		
		if (frm.is_new()) {
			let monthes = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' , 'October' , 'November' , 'December']
			const today = new Date();
			let month = today.getMonth(); // returns from 0 to 11
			frm.doc.month = monthes[month];

			const d = new Date();
			let year = d.getFullYear();
			frm.doc.year = year

			frm.refresh_fields();
		};
	},
	
	get_employees(frm) {
		cur_frm.clear_table("employee_table");
		frappe.call({
			method :"get_employees",
			doc:frm.doc,
			args: {},
			callback:function(r){
				if(r.message){
					console.log(r.message);
					frm.refresh_field("employee_table");
				}
			}
		});
	},
});
