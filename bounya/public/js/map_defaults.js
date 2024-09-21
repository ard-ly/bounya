// Make sure we have a dictionary to add our custom settings
const map_settings = frappe.provide("frappe.utils.map_defaults");

// Center and zoomlevel can be copied from the URL of
// the map view at openstreetmap.org.

// New default location (middle of germany).
map_settings.center = [32.885353, 13.180161]; //Tripoli, Libya

// new zoomlevel: see the whole country, not just a single city
map_settings.zoom = 6;

