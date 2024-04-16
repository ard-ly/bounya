// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Application Group', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1){
			frm.set_df_property("get_employees", "hidden", 1);
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
					frm.refresh_field("employees_table");
					frm.refresh_fields();
					frm.refresh();
				}
			}
		});
	},
});
