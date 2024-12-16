// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Incoming Mail', {
	onload: function(frm) {
		if(frm.doc.docstatus==0){
			frappe.call({
	            method: 'frappe.client.get_list',
	            args: {
	                doctype: 'Department',
	                filters: { 'custom_is_board_of_directors': 1 },
	                fields: ['name']
	            },
	            callback: function (response) {
	                if (response.message) {
	                    let departments = response.message;
	                    
	                    let existingDepartments = [];
			            $.each(frm.doc.copy_to || [], function (i, d) {
			            	existingDepartments.push(d.department);
						});

	                    departments.forEach(dept => {
	                        if (dept.name && !existingDepartments.includes(dept.name)) {
	                            let newRow = frm.add_child('copy_to', {
	                                department: dept.name
	                            });
	                        }
	                    });

	                    frm.refresh_field('copy_to');
	                }
	            }
	        });
	    }


		frm.set_query('decision_number', function () {
            return {
                filters: {
                    docstatus: 1
                }
            };
        });

        frm.set_query('outgoing_mail', function () {
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
	outgoing_email_referral: function(frm) {
		frm.set_value("outgoing_mail", )
		frm.set_value("outgoing_message_subject", )
	},
	transfer_type: function(frm) {
		frm.set_value("from", )
		frm.set_value("to", )
	}
});
