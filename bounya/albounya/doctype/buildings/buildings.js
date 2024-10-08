// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Buildings', {
	onload: function(frm) {
		frm.set_query("asset", function() {
			return {
				filters: {
					"docstatus": 0,
					"custom_is_building": 1,
					// "asset_category": "Buildings",
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
	refresh(frm) {

		if (frm.doc.latitude && frm.doc.longitude) {
            frm.doc.geolocation = `{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[${frm.doc.longitude},${frm.doc.latitude}]}}]}`;
            frm.refresh_fields();
            // Ensure the map is available and initialized
            if (frm.fields_dict.geolocation.map) {
                let map = frm.fields_dict.geolocation.map;
        
                if (map) {
                    // Remove the previous marker if it exists
                    if (frm.marker) {
                        map.removeLayer(frm.marker);
                    }
        
                    // Add a new marker at the current location (make sure the order is [longitude, latitude])
                    frm.marker = L.marker([frm.doc.latitude, frm.doc.longitude]).addTo(map);
        
                    // Optionally, bind a popup to the marker
                    frm.marker.bindPopup("Your location").openPopup();
        
                    // Center the map on the new marker
                    map.setView([frm.doc.latitude, frm.doc.longitude], 13);
                }
            }
    
            // Correct the order of latitude and longitude in GeoJSON
        }
        frm.refresh_fields();
        console.log(frm.doc.geolocation);





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
frappe.listview_settings['Buildings'] = {
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
			label: 'Buildings', //the name of the field in Doc 2 that points to Doc 1
			route: '/app/assets/Buildings',
	});
	 	},
	}
