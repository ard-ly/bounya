// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Uninstall Equipment', {
	before_submit: function(frm) {
		if (frm.doc.uninstalled == 0){
			frappe.throw(__("Can not submit if Equipment are not uninstalled."));
		}
	},
	
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
				frm.doc.owner1 = eq_doc.owned_by;
				frm.doc.tower = eq_doc.tower;
				if(eq_doc.equipment_table){
					frm.set_value('uninstall_equipment_table_tab', []);
					eq_doc.equipment_table.forEach((row)=>{
                            var child = frm.add_child('uninstall_equipment_table_tab');
                            child.equipment_name = row.equipment_name;
                            child.manufacturer = row.manufacturer;
							child.serial_number = row.serial_number;
                        });

					}
				frm.refresh_fields();
			});
		}
	},
});
