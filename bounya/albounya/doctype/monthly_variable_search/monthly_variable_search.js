// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Variable Search', {
	// refresh: function(frm) {

	// },
	month(frm) {
		if (frm.doc.month) {

			const d = new Date();
			let year = d.getFullYear();
			// console.log(`${year}`);

			let month = frm.doc.month
			var dateString = '' + year + '-' + month + '-' + '25';
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
			args: {
				from_date : frm.doc.from_date,
				to_date: frm.doc.to_date,
			},
			callback:function(r){
				if(r.message){
					console.log(r.message);
					frm.refresh_field("monthly_variables_settings");
					frm.refresh_fields();
					frm.refresh();
					frm.refresh();
					
				}
			}
		});
	},
});
