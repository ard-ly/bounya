// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Realty', {
	validate: function(frm) {
		let naming = frm.doc.realty_no

		if (frm.doc.location){
			naming = naming + "/" +frm.doc.location
		}
		if (frm.doc.office_no){
			naming = naming + "/" +frm.doc.office_no
		}
		if (frm.doc.branch_no){
			naming = naming + "/" +frm.doc.branch_no
		}
		frm.doc.realty_name = naming;
		frm.refresh_field("realty_name");

		if (frm.doc.realty_ct){
			let total = 0.0
			frm.doc.realty_ct.forEach((d) => {
				total += d.covered_space;
			});
			frm.doc.covered_space = total;
			frm.refresh_field("covered_space");
		}
	},
	
	onload: function(frm) {
		frm.set_query("building", function() {
			return {
				filters: {
					"docstatus": 1,
				}
			};
		});
		frm.set_query("towers", function() {
			return {
				filters: {
					"docstatus": 1,
				}
			};
		});
		

	},
	// covered_space:function(frm) {
	// 	if ((frm.doc.docstatus != 1) || (frm.doc.docstatus != 2)){
	// 			frm.doc.available_area = frm.doc.covered_space;
	// 			frm.refresh_field("available_area");
			
	// 	}
	// },

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

	branch: function(frm) {
		frm.set_query("office", function() {
			return {
				query: "bounya.queries.filter_office",
				filters: {
					branch: frm.doc.branch
				}
			};
		});
	},

	building: function(frm){
		if (frm.doc.building){
			frappe.db.get_doc('Buildings', frm.doc.building).then(building_doc => {
				frm.doc.number_of_floors = building_doc.number_of_floors;
				frm.doc.branch = building_doc.branch;
				frm.doc.office = building_doc.office;
				frm.doc.coordinates = building_doc.geolocation;
				frm.doc.description = building_doc.details;
				frm.refresh_fields();
			});
		}

	},

	towers: function(frm){
		if (frm.doc.towers){
			frappe.db.get_doc('Towers', frm.doc.towers).then(towers_doc => {
				frm.doc.branch = towers_doc.branch;
				frm.doc.office = towers_doc.office;
				frm.doc.coordinates = towers_doc.geolocation;
				frm.doc.description = towers_doc.details;
				frm.refresh_fields();
			});
		}
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
