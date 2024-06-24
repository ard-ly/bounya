// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee External Advance', {
	setup: function(frm) {
		// filter on employee.
		frm.set_query("employee", function() {
			return {
				filters: {
					"status": "Active"
				}
			};
		});

		if (frm.is_new()) {
			const today = new Date();
			frm.doc.posting_date = today;
			frm.refresh_field("posting_date");
		};
	},

	before_submit: function(frm) {
		frm.doc.status = 'Unpaid';
		frm.refresh_field("status");
	},
	
	after_cancel: function(frm) {
		frm.refresh_field("status");
	},
});
