// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Realty', {
	
	refresh: frm => {

		if (frm.doc.docstatus  == 1){
			frm.add_custom_button(__('Salary structure Assignment'), function () {
				frappe.model.open_mapped_doc({
					method: "bounya.albounya.doctype.realty.realty.create_asset",
					frm: frm,
				})
			}, __("Make"));
	}
		// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
		frappe.breadcrumbs.clear();
				
		// Now add breadcrumb for the 'parent' document
				frappe.breadcrumbs.set_custom_breadcrumbs({
						label: cur_frm.doc.doctype, //the name of the field in Doc 2 that points to Doc 1
						route: '/app/' + cur_frm.doc.doctype.toLowerCase().replace(/ /g, "-"),
						});

				// Finally add the breadcrumb for this document  
				frappe.breadcrumbs.set_custom_breadcrumbs({
						label: cur_frm.doc.name,
						route: '/app/' + cur_frm.doc.doctype.toLowerCase().replace(/ /g, "-") + '/' + cur_frm.doc.name.replace(/ /g, "-"),
						});

	},


});
frappe.listview_settings['Append'] = {
    refresh: function (listview) {
			// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
		frappe.breadcrumbs.clear();				
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
			label: 'Assets', //the name of the field in Doc 2 that points to Doc 1
			route: '/app/Assets',
		});
				
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
				label: 'Realty', //the name of the field in Doc 2 that points to Doc 1
				route: '/app/assets/Realty',
		});
		},
}
