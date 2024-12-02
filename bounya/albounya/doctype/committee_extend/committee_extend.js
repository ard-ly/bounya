// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Committee Extend', {
	onload(frm) {
        frm.set_query("committee", function() {
            return {
                filters: [
                    ["Committees","docstatus", "=", 1]
                ]
            }
        });
    },
    validate(frm) {
		frm.events.validate_committee_dates(frm);
    },
    committee_extend_from(frm) {
		frm.events.validate_committee_dates(frm);
    },
    committee_extend_to(frm) {
		frm.events.validate_committee_dates(frm);
    },
    validate_committee_dates(frm) {
        let committee_extend_from = frm.doc.committee_extend_from;
        let committee_extend_to = frm.doc.committee_extend_to;

        if (committee_extend_from && committee_extend_to && committee_extend_from > committee_extend_to) {
            frappe.msgprint(__('Committee From date must be less than or equal to Committee To date.'));
            
            frappe.validated = false;
        }
    }
});
