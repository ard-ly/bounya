frappe.ui.form.on('Lead', {

    validate: function (frm) {
        const today = new Date();
        if(frm.doc.custom_minimum_qualification_score > 0){
            
            if(frm.doc.custom_total_grades < frm.doc.custom_minimum_qualification_score){
                frm.doc.qualification_status = "Unqualified";
                frm.doc.qualified_by = frappe.user.name;
                frm.doc.qualified_on = today;
               
                if (frm.doc.custom_equipment_installation_form_doctype){
                    frappe.call({
                        method :"bounya.api.send_qualification_notification",
                        args: {
                            doc_name: frm.doc.name,
                            status:"Unqualified",
                        },
                        callback:function(r){
                            if(r.message){
                                console.log(r.message);
                            }
                        }
                    });
                }
                frm.refresh_fields();
            }

            else{
                frm.doc.qualification_status = "Qualified";
                frm.doc.qualified_by = frappe.user.name;
                frm.doc.qualified_on = today;

                if (frm.doc.custom_equipment_installation_form_doctype){
                    frappe.call({
                        method :"bounya.api.send_qualification_notification",
                        args: {
                            doc_name: frm.doc.name,
                            status:"Qualified",
                        },
                        callback:function(r){
                            if(r.message){
                                console.log(r.message);
                            }
                        }
                    });
                }
                frm.refresh_fields();
            }
        }
    },

    custom_qualification_template:function (frm) {
        if (frm.doc.custom_qualification_template){
            frm.set_value('custom_qualification_grade_table', []);
            frappe.call({
                method :"bounya.api.get_qualification",
                args: {
                    qualification_template: frm.doc.custom_qualification_template,
                },
                callback:function(r){
                    if(r.message){
                        console.log(r.message.q_list);

                        r.message.q_list.forEach((row)=>{
                            var child = frm.add_child('custom_qualification_grade_table');
                            child.qualification = row;
                            child.grade = 0;
                        });

                        frm.refresh_fields();
                    }
                }
            });
        }
    },

    refresh:function (frm) {
        if (frm.doc.docstatus  == 0){
			frm.add_custom_button(__('Opportunity'), function () {
                
                if (frm.doc.qualification_status == 'Qualified'){
                    if (frm.doc.custom_equipment_installation_form == 1){
                        frappe.model.open_mapped_doc({
                        	method: "bounya.api.create_opportunity_from_lead",
                        	frm: frm,
                            args: {
                               "owner":frappe.user,

                            }
                        })
                    }
                    else{
                        // 1.prospect.
                        // 2. Opportunity form == Lead.
                        frm.trigger("make_opportunity");
                     
                    }
                }
                else{
                    frappe.throw(__("Lead must be Qualified to create Opportunity."));
                }
			}, __("Create"));
	}
    },

    make_opportunity: async function(frm) {
		let existing_prospect = (await frappe.db.get_value("Prospect Lead",
			{
				"lead": frm.doc.name
			},
			"name", null, "Prospect"
		)).message.name;

		if (!existing_prospect) {
			var fields = [
				{
					"label": "Create Prospect",
					"fieldname": "create_prospect",
					"fieldtype": "Check",
					"default": 1
				},
				{
					"label": "Prospect Name",
					"fieldname": "prospect_name",
					"fieldtype": "Data",
					"default": frm.doc.company_name,
					"depends_on": "create_prospect"
				}
			];
		}
		let existing_contact = (await frappe.db.get_value("Contact",
			{
				"first_name": frm.doc.first_name || frm.doc.lead_name,
				"last_name": frm.doc.last_name
			},
			"name"
		)).message.name;

		if (!existing_contact) {
			fields.push(
				{
					"label": "Create Contact",
					"fieldname": "create_contact",
					"fieldtype": "Check",
					"default": "1"
				}
			);
		}

		if (fields) {
			var d = new frappe.ui.Dialog({
				title: __('Create Opportunity'),
				fields: fields,
				primary_action: function() {
					var data = d.get_values();
					frappe.call({
						method: 'create_prospect_and_contact',
						doc: frm.doc,
						args: {
							data: data,
						},
						freeze: true,
						callback: function(r) {
							if (!r.exc) {
								frappe.model.open_mapped_doc({
									method: "erpnext.crm.doctype.lead.lead.make_opportunity",
									frm: frm
								});
							}
							d.hide();
						}
					});
				},
				primary_action_label: __('Create')
			});
			d.show();
		} else {
			frappe.model.open_mapped_doc({
				method: "erpnext.crm.doctype.lead.lead.make_opportunity",
				frm: frm
			});
		}
	}
});

frappe.ui.form.on('Qualification Grade Table', {
    grade: function(frm, cdt, cdn) {
        let grade_sum = 0
        frm.doc.custom_qualification_grade_table.forEach((row)=>{
            grade_sum += row.grade
        });
        frm.doc.custom_total_grades = grade_sum;
        frm.refresh_fields();
    },

    custom_qualification_grade_table_remove:function(frm, cdt, cdn) {
        let grade_sum = 0
        frm.doc.custom_qualification_grade_table.forEach((row)=>{
            grade_sum += row.grade
        });
        frm.doc.custom_total_grades = grade_sum;
        frm.refresh_fields();
    },
});
