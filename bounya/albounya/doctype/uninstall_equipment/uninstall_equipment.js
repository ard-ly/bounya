// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Uninstall Equipment', {
	onload: function(frm) {
		frm.set_query("equipment_installation", function() {
			return {
				filters: {
					"docstatus": 1,
					
				}
			};
		});

	},
	equipment_installation:function(frm) {
		if (frm.doc.equipment_installation){
			frappe.db.get_doc('Equipment Installation', frm.doc.equipment_installation).then(eq_doc => {
				frm.doc.equipment_name = eq_doc.equipment_name;
				frm.doc.technical_name = eq_doc.technical_name;
				frm.doc.serial_number = eq_doc.serial_number;
				frm.refresh_fields();
			});
		}
	},
});
