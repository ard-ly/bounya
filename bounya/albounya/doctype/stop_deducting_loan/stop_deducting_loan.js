// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stop Deducting Loan', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1){
			frm.set_df_property("get_employees", "hidden", 1);
		}
		// frm.set_query("loan", function () {
		// 	return {
		// 	  filters: [
		// 		["Loan", 'docstatus', '=', 1 ],
				
		// 	  ],
		// 	};
		//   });
	},

	get_employees(frm) {
		frappe.call({
			method :"get_employees",
			doc:frm.doc,
			args: {
				start_date : frm.doc.start_date,
				end_date: frm.doc.end_date,
			},
			callback:function(r){
				if(r.message){
					console.log(r.message);
					frm.refresh_field("stop_deducting_employees");
					frm.refresh_fields();
					frm.refresh();
					
				}
			}
		});
	},
});

