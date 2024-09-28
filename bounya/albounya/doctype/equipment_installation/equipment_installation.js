// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Installation', {
	// installed
	
	before_submit: function(frm) {
		if (frm.doc.installed == 0){
			frappe.throw(__("Can not submit if Equipment is not installed."));
		}
	},
	
	onload: function(frm) {
		frm.set_query("sales_order", function() {
			return {
				filters: {
					"docstatus": 1,
					// "order_type": "Equipment Installation",
				}
			};
		});
		 
		frm.set_query("contract", function() {
			return {
				filters: {
					"docstatus": 1,
					"document_type":  ["in", ["Sales Order","Quotation"]],
				}
			};
		});
	},

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
frappe.listview_settings['Equipment Installation'] = {
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
			label: 'Equipment Installation', //the name of the field in Doc 2 that points to Doc 1
			route: '/app/assets/Equipment Installation',
	});
	},
	}


