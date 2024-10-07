// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Towers', {
	onload: function(frm) {
		
		frm.set_query("asset", function() {
			return {
				filters: {
					"docstatus": 0,
					"custom_is_tower": 1,
				}
			};
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

	total_area:function(frm) {
		if ((frm.doc.docstatus != 1) || (frm.doc.docstatus != 2)){
			// if(frm.doc.total_area > 0){
				frm.doc.available_area = frm.doc.total_area;
				frm.refresh_field("available_area");
			// }
		}
	},

	refresh(frm) {

		if (frm.doc.latitude && frm.doc.longitude) {
            // Ensure the map is available
            if (frm.fields_dict.location.map) {
                let map = frm.fields_dict.location.map;
                
                // If a previous marker exists, remove it
                if (frm.marker) {
                    map.removeLayer(frm.marker);
                }

                // Add a new marker at the current location
                frm.marker = L.marker([frm.doc.latitude, frm.doc.longitude]).addTo(map);

                // Optionally, bind a popup to the marker
                frm.marker.bindPopup("Your location").openPopup();

                // Center the map to the new marker
                map.setView([frm.doc.latitude, frm.doc.longitude], 13);  // '13' is the zoom level
            }
        }

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
frappe.listview_settings['Towers'] = {
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
			label: 'Towers', //the name of the field in Doc 2 that points to Doc 1
			route: '/app/assets/Towers',
	});
	},
	}
