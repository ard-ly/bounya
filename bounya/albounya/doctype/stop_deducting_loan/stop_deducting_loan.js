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

		//   if (frm.doc.docstatus == 1) {
		// 	frm.add_custom_button(
		// 	  __("Clarification Form"),
		// 	  function () {
		// 		frappe.model.open_mapped_doc({
		// 		  method: "arc.api.make_clarification_form",
		// 		  frm: frm,
		// 		});
		// 	  },
		// 	  __("Create")
		// 	);
		//   }
	  

	}
});

