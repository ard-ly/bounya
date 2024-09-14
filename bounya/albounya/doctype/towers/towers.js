// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Towers', {
	onload: function(frm) {
		frm.set_query("asset", function() {
			return {
				filters: {
					"docstatus": 0,
					"custom_is_tower": 1,
					// "asset_category": "Towers",
				}
			};
		});
	},
	branch: function(frm) {
		frm.set_query("office", function() {
			return {
				query: "bounya.queries.filter_office",
				filters: {
					branch: frm.doc.branch
				}
			};
		});
	}
});
