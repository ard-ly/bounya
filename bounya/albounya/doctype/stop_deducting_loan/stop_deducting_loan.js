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

	}
});

