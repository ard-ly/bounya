// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stop Deducting Loan', {
	refresh: function(frm) {
		frm.set_query("loan", function () {
			return {
			  filters: [
				["Loan", 'docstatus', '=', 1 ],
				
			  ],
			};
		  });

		//   if (frm.doc.docstatus != 1) {
		// 	frm.add_custom_button(
		// 	  __("Get Employess"),
		// 	  function () {
		// 		frappe.model.open_mapped_doc({
		// 		  method: "",
		// 		  frm: frm,
		// 		});
		// 	  },
		// 	);
		//   }
	  

	},

	get_employees(frm) {
		frappe.call({
			method :"get_employees",
			doc:frm.doc,
			callback:function(r){
				if(r.message){
					console.log("aaaaaaaaaaaaaaaaaaaaaaaaa");
					console.log(r.message);
					
				}
			}
		});
	},
});

