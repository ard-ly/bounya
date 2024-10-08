// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt


frappe.ui.form.on('Realty Location', {

	refresh: function(frm) {
        if (frm.doc.latitude && frm.doc.longitude) {
            // Ensure the map is available
            if (frm.fields_dict.location_coordinates.map) {
                let map = frm.fields_dict.location_coordinates.map;
                
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
