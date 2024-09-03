// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Installation', {
	onload: function(frm) {
		frm.set_query("equipment_installation", function() {
			return {
				filters: {
					"docstatus": 1,
				}
			};
		});

		frm.set_query("sales_order", function() {
			return {
				filters: {
					"docstatus": 1,
					"order_type": "Towers",
				}
			};
		});
	},
	
});
