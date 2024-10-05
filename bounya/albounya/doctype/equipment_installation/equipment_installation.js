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
					"document_type":  "Sales Order",
					"document_name": frm.doc.sales_order,
					"is_signed": 1,

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
	
	contract(frm) {
		if (frm.doc.contract){
			frappe.db.get_doc('Contract', frm.doc.contract).then(contract_doc => {
				if (contract_doc.custom_equipment_installation_form){
					frappe.db.get_doc('Equipment Installation Form', contract_doc.custom_equipment_installation_form).then(eq_form_doc => {
						frm.doc.tower= eq_form_doc.tower;
						frm.doc.owned_by = eq_form_doc.customer;
						frm.refresh_fields();
						// frm.doc.equipment_name = eq_form_doc.
						// frm.doc.technical_name
						// frm.doc.equipment_radius
						// frm.doc.equipment_height
						// frm.doc.equipment_weigh
						// frm.doc.equipment_direction
						// frm.doc.direction_degrees
					});
				}
			});
		}
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


