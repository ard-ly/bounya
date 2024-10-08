// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt


frappe.ui.form.on('Realty Location', {

	refresh: function(frm) {
        if (frm.doc.latitude && frm.doc.longitude) {
            // Ensure the map is available and initialized
            if (frm.fields_dict.location_coordinates.map) {
                let map = frm.fields_dict.location_coordinates.map;
        
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
            frm.doc.location_coordinates = `{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[${frm.doc.longitude},${frm.doc.latitude}]}}]}`;
        }
        frm.refresh_fields();
        console.log(frm.doc.location_coordinates);
    }
});

// [12.418213,32.475167]
// '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[12.418213,32.475167]}}]}'
// {  
// 	"type":"Feature",
// 	"properties":{  
// 	   "point_type":"circle",
// 	   "radius":1976.1269632232793
// 	},
// 	"geometry":{  
// 	   "type":"Point",
// 	   "coordinates":[  
// 		  72.854548,
// 		  19.096511
// 	   ]
// 	}
//  },
