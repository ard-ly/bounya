// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Outgoing Mail', {
	// validate: function (frm) {
    //     (frm.doc.marginalize || []).forEach(row => {
    //         if (!row.employee && row.owner) {
    //             frappe.call({
    //                 method: 'frappe.client.get_value',
    //                 args: {
    //                     doctype: 'Employee',
    //                     filters: { user_id: row.owner },
    //                     fieldname: 'name'
    //                 },
    //                 async: false,
    //                 callback: function (response) {
    //                     if (response.message && response.message.name) {
    //                         row.employee = response.message.name;

    //                         frappe.call({
    //                             method: 'frappe.client.get_value',
    //                             args: {
    //                                 doctype: 'Department',
    //                                 filters: { custom_department_manager: row.employee },
    //                                 fieldname: 'name'
    //                             },
    //                             async: false,
    //                             callback: function (dept_response) {
    //                                 if (dept_response.message) {
    //                                     row.department = dept_response.message.name;
    //                                 }
    //                             }
    //                         });
    //                     }
    //                 }
    //             });
    //         }
    //     });
    // },
	refresh: function(frm) {
		if (frm.doc.docstatus === 1) {
            frm.page.sidebar.find('.attachments-actions').hide(); // Hide the "Add Attachment" button
            frm.page.sidebar.find('.attachment-row .btn .remove-btn').hide(); // Hide the delete icon for attachments
        }
	},
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

	    if(!frm.doc.entity){
	    	frappe.call({
		        method: "get_session_office_manager_user_entity",
		        doc: cur_frm.doc,
		        callback: function(r) {
		        	if(r.message){
		        		frm.set_value("entity", r.message)
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
		
		frm.set_query('incoming_mail', function () {
            return {
                filters: {
                    docstatus: 1
                }
            };
        });

	},
	decision: function(frm) {
		frm.set_value("decision_number", )
		frm.set_value("decision_date", )
		frm.set_value("decision_file", )
	},
	incoming_email_referral: function(frm) {
		frm.set_value("incoming_mail", )
		frm.set_value("incoming_message_subject", )
	},
	entity: function(frm) {
		if(frm.doc.entity && !frm.doc.from){
			frm.set_value("from", frm.doc.entity)
		}
	},
	to: function(frm) {
		if(frm.doc.to && !frm.doc.referral_to){
			frm.set_value("referral_to", frm.doc.to)
		}
	}
});



// frappe.ui.form.on('Marginalize User', {
//     marginalize: function (frm, cdt, cdn) {
//         let row = frappe.get_doc(cdt, cdn);

//         if (!row.employee) {
//             frappe.call({
//                 method: 'frappe.client.get_value',
//                 args: {
//                     doctype: 'Employee',
//                     filters: { user_id: frappe.session.user },
//                     fieldname: 'name'
//                 },
//                 callback: function (response) {
//                     if (response.message) {
//                         frappe.model.set_value(cdt, cdn, 'employee', response.message.name);

//                         frappe.call({
//                             method: 'frappe.client.get_value',
//                             args: {
//                                 doctype: 'Department',
//                                 filters: { custom_department_manager: response.message.name },
//                                 fieldname: 'name'
//                             },
//                             callback: function (dept_response) {
//                                 if (dept_response.message) {
//                                     frappe.model.set_value(cdt, cdn, 'department', dept_response.message.name);
//                                 }
//                             }
//                         });

//                     }
//                 }
//             });
//         }

//     }
// });



