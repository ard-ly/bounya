frappe.ui.form.on('Material Request', {
	refresh(frm) {
		// your code here
		if (frm.doc.workflow_state == 'رفض مدير وحدة المخازن') {
			frm.add_custom_button(__("Purchase Material Request"), function() {

			        }, __("Create"));
				}
	},
	custom_cost_center(frm, cdt, cdn) {
		// var row = locals[cdt][cdn];
        // frappe.msgprint('okok');
		erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "cost_center");
	},
	custom_project(frm, cdt, cdn) {
		erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "project");
	},
})
