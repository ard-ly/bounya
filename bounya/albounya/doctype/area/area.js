// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Area', {

		refresh(frm) {
			// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
					frappe.breadcrumbs.clear();
					
			// Now add breadcrumb for the 'parent' document
					frappe.breadcrumbs.set_custom_breadcrumbs({
							label: cur_frm.doc.doctype, //the name of the field in Doc 2 that points to Doc 1
							route: '/app/' + frappe.scrub(cur_frm.doc.doctype).replace('_', '-'),
							});
	
					// Finally add the breadcrumb for this document  
					frappe.breadcrumbs.set_custom_breadcrumbs({
							label: cur_frm.doc.name,
							route: '/app/' + frappe.scrub(cur_frm.doc.doctype).replace('_', '-') 
							});
	
		},
});
frappe.listview_settings['Area'] = {
    refresh: function (listview) {
			// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
		frappe.breadcrumbs.clear();				
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
				label: 'Accounting', //the name of the field in Doc 2 that points to Doc 1
				route: '/app/accounting',
		});
				
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
				label: 'Area', //the name of the field in Doc 2 that points to Doc 1
				route: '/app/area',
		});
		},
}
