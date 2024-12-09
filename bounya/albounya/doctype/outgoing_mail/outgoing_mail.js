// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Outgoing Mail', {
	onload: function(frm) {
		frm.set_query('decision_number', function () {
            return {
                filters: {
                    docstatus: 1
                }
            };
        });

		frm.set_query('transfer_type', function () {
            return {
                filters: [
                    ['name', 'in', ['Designation', 'Department']]
                ]
            };
        });
	},
	decision: function(frm) {
		frm.set_value("decision_number", )
		frm.set_value("decision_date", )
		frm.set_value("decision_file", )
	},
	transfer_type: function(frm) {
		frm.set_value("from", )
		frm.set_value("to", )
	}
});
