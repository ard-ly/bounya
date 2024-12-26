// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Decisions', {
	refresh: function(frm) {
		frm.set_query('previous_decision_number', function () {
            return {
                filters: {
                    docstatus: 1
                }
            };
        });
	}
});
