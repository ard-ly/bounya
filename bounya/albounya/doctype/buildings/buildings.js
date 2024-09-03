// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Buildings', {
	onload: function(frm) {
		frm.set_query("asset", function() {
			return {
				filters: {
					"docstatus": 0,
					"asset_category": "Buildings",
				}
			};
		});
	},
});