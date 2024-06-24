// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('External Loans Type', {
	setup: function(frm) {
		// filter on employee.
		frm.set_query("salary_component", function() {
			return {
				filters: {
					"type": "Deduction"
				}
			};
		});
	},
});
