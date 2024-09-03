// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stop Deducting Loan', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1){
			frm.set_df_property("get_employees", "hidden", 1);
		}
	
	},
	refresh: function(frm) {
		frm.fields_dict['stop_deducting_employees'].grid.get_field('loan').get_query = function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			//console.log(child);
			return {    
				filters:[
					['applicant', '=', child.employee]
				]
			}
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
					frm.refresh_field("stop_deducting_employees");
					
				}
			}
		});
	},
});

