// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("Committees", {
    refresh(frm) {
        if(frm.doc.docstatus==1){
            frm.add_custom_button(__('Committee Extend'), () => {
                frappe.route_options = {
                    "committee": frm.doc.name
                };
                frappe.set_route("committee-extend", "new-committee-extend");
            });
        }
    },
    validate(frm) {
        frm.events.validate_committee_dates(frm);
        frm.events.validate_committee_decision_dates(frm);
    },
    committee_from(frm) {
		frm.events.validate_committee_dates(frm);
        frm.events.validate_committee_decision_dates(frm);
    },
    committee_to(frm) {
		frm.events.validate_committee_dates(frm);
        frm.events.validate_committee_decision_dates(frm);
    },
    validate_committee_dates(frm) {
        let committee_from = frm.doc.committee_from;
        let committee_to = frm.doc.committee_to;

        if (committee_from && committee_to && committee_from > committee_to) {
            frappe.msgprint(__('Committee From date must be less than or equal to Committee To date.'));
            
            frappe.validated = false;
        }
    },
    validate_committee_decision_dates(frm) {
        let committee_from = frm.doc.committee_from;
        let committee_to = frm.doc.committee_to;

        let decision_date = frm.doc.decision_date;

        if (committee_from < decision_date) {
            frappe.msgprint(__('Committee From date must be more than or equal to Decision date.'));
            frm.set_value("committee_from",)
            frappe.validated = false;
        }
        if (committee_to < decision_date) {
            frappe.msgprint(__('Committee To date must be more than or equal to Decision date.'));
            frm.set_value("committee_to",)
            frappe.validated = false;
        }
    }
});


frappe.ui.form.on("Committee Prosecutor","employee", function(frm, cdt, cdn) {
    var row = locals[cdt][cdn];

    if (row.employee) {
        frappe.call({
            doc: cur_frm.doc,
            args: {
                employee_name: row.employee
            },
            method: "get_employee_data",
            callback: function(r) {
                if(r.message){
                    frappe.model.set_value(cdt, cdn, "member_name", r.message['employee_name']);
                    frappe.model.set_value(cdt, cdn, "designation", r.message['designation']);
                    frappe.model.set_value(cdt, cdn, "adjective", r.message['designation']);
                    frappe.model.set_value(cdt, cdn, "email", r.message['prefered_email']);
                    frappe.model.set_value(cdt, cdn, "phone_number", r.message['cell_number']);

                    frm.refresh_field('committee_table');
                }
            }
        });
    }

});




