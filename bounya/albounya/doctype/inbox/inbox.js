// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inbox', {
	onload: function(frm) {
		frm.set_query('mail_type', function () {
            return {
                filters: [
                    ['name', 'in', ['Incoming Mail', 'Outgoing Mail']]
                ]
            };
        });
    },
});
