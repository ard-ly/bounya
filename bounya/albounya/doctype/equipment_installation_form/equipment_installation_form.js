// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Installation Form', {
	onload: function(frm) {
		if (frappe.user.has_role("Customer")){
			
			// frappe.db.get_doc('User', frappe.user.name).then(user_doc => {
					// frm.set_df_property("customer", "hidden", 1);
			// 		frm.doc.customer_name = user_doc.full_name;
					// frm.doc.user = frappe.user.name;
					// frm.set_df_property("email", "hidden", 1);
			// 		frm.doc.email = user_doc.email;
			// 		frm.refresh_fields();
				
			// });
		}
	},

	branch: function(frm) {
		frm.set_query("towers", function() {
			return {
				filters: {
					"docstatus": 1,
					"branch": frm.doc.branch,
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

frappe.listview_settings['Equipment Installation Form'] = {
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
			route: '/app/assets/Equipment Installation Form',
	});
	},
	}

