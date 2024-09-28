// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Installation Form', {
	onload: function(frm) {
		
		frm.set_query("towers", function() {
			return {
				filters: {
					"docstatus": 1,
					"allow_equipment_installation":1,
				}
			};
		});

		frm.doc.user = frappe.user.name;
		frm.refresh_fields();

		if (frappe.user != 'Administrator'){
			if (frappe.user.has_role("Customer")){	
				frm.set_query("customer", function() {
					return {
						query: "bounya.queries.filter_customer_based_on_users",
						filters: {
							user: frappe.user.name,
						}
					};
				});
				// frm.doc.querySelector('.layout-side-section').style.display = 'none';
			}
		}
	},

	refresh(frm) {
		// if (frappe.user.has_role("Customer")){
		// 	frm.doc.querySelector('.layout-side-section').style.display = 'none';
		// }

	// 	// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
	// 			frappe.breadcrumbs.clear();
				
	// 	// Now add breadcrumb for the 'parent' document
	// 			frappe.breadcrumbs.set_custom_breadcrumbs({
	// 					label: cur_frm.doc.doctype, //the name of the field in Doc 2 that points to Doc 1
	// 					route: '/app/' + frappe.scrub(cur_frm.doc.doctype).replace('_', '-'),
	// 					});

	// 			// Finally add the breadcrumb for this document  
	// 			frappe.breadcrumbs.set_custom_breadcrumbs({
	// 					label: cur_frm.doc.name,
	// 					route: '/app/' + frappe.scrub(cur_frm.doc.doctype).replace('_', '-') 
	// 					});

	},
});

frappe.listview_settings['Equipment Installation Form'] = {

	onload: function(listview) {
		if (frappe.user != 'Administrator'){
			if (frappe.user.has_role("Customer")){	
				listview.page.add_inner_button('Clear Filters', function() {
					listview.filter_area.clear();
				});

				// Set default filters
				listview.filter_area.add([
					['Equipment Installation Form', 'user', '=', frappe.user.name]
				]);
			}
		}
	}

	// refresh: function (listview) {
	// 	// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
	// 	frappe.breadcrumbs.clear();				
	// 	// Now add breadcrumb for the 'parent' document
	// 	frappe.breadcrumbs.set_custom_breadcrumbs({
	// 		label: 'Assets', //the name of the field in Doc 2 that points to Doc 1
	// 		route: '/app/Assets',
	// 	});
			
	// 	// Now add breadcrumb for the 'parent' document
	// 	frappe.breadcrumbs.set_custom_breadcrumbs({
	// 			label: 'Equipment Installation Form', //the name of the field in Doc 2 that points to Doc 1
	// 			route: '/app/Equipment Installation Form',
	// 	});
	// },
	}

