// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee External Loans', {
	
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
			frm.doc.status = 'Draft';
			frm.refresh_field("status");
		};
	},
	
	refresh: function(frm) {
		if (frm.doc.paid_amount = 0){
			frm.doc.remaining_amount = frm.doc.advance_amount;
			frm.refresh_field("remaining_amount");
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
