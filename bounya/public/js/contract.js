frappe.ui.form.on('Contract', {
    on_submit: function (frm) {
        frappe.call({
            method :"bounya.api.send_contract_notification",
            args: {
                doc_name: frm.doc.name,
            },
            callback:function(r){
                if(r.message){
                    console.log(r.message);
                }
            }
        });
    },
    
    onload(frm){
        let types = ["Customer","Supplier"];
        frm.set_df_property("party_type", "options", types);
        frm.refresh_field("party_type");
    },

    custom_company(frm){
        if (frm.doc.custom_company){

            frappe.call({
                method: "bounya.api.get_address_html",
                args: {
                    link_doctype: "company",
                    link_name : frm.doc.custom_company,
                },
                frm: frm,
                callback: r => {
                    if (r.message){
                        console.log(r.message);
                        frm.doc.custom_first_party_address_html =  r.message;
                        frm.refresh_field("custom_first_party_address_html");
                    }
                }
            })
            
        }
    },

    party_name(frm){
        if (frm.doc.party_name){

            frappe.call({
                method: "bounya.api.get_address_html",
                args: {
                    link_doctype: frm.doc.party_type,
                    link_name : frm.doc.party_name,
                },
                frm: frm,
                callback: r => {
                    if (r.message){
                        console.log(r.message);
                        frm.doc.custom_second_party_address_html =  r.message;
                        frm.refresh_field("custom_second_party_address_html");
                    }
                }
            });
            
            frappe.call({
                method: "bounya.api.get_party_contact",
                args: {
                    link_doctype: frm.doc.party_type,
                    link_name : frm.doc.party_name,
                },
                frm: frm,
                callback: r => {
                    if (r.message){
                        console.log(r.message);
                        frm.doc.party_user = r.message.user;
                        frm.refresh_field("party_user");
                        frm.doc.custom_second_party_phone = r.message.phone;
                        frm.refresh_field("custom_second_party_phone");
                    }
                }
            });
            
        }
    },
    document_name(frm){
        if (frm.doc.document_name){  
            if (frm.doc.document_type == "Purchase Invoice"){
                frappe.db.get_doc("Purchase Invoice", frm.doc.document_name).then(docu => { 
                    frm.doc.party_type ="Supplier";
                    frm.doc.party_name = docu.supplier;
                    frm.trigger('party_name');
                    frm.doc.custom_service_value = docu.total;  
                    frm.doc.custom_tax = docu.total_taxes_and_charges;
                    frm.doc.custom_total = docu.grand_total;
                    
                    frm.refresh_fields();
                });
            }
            else if(frm.doc.document_type == "Purchase Order"){
                frappe.db.get_doc("Purchase Order", frm.doc.document_name).then(docu => { 
                    frm.doc.party_type ="Supplier";
                    frm.doc.party_name = docu.supplier;
                    frm.trigger('party_name');
                    frm.doc.custom_service_value = docu.total;  
                    frm.doc.custom_tax = docu.total_taxes_and_charges;
                    frm.doc.custom_total = docu.grand_total;
                    frm.refresh_fields();
                });
            }
            else if(frm.doc.document_type == "Sales Invoice"){
                frappe.db.get_doc("Sales Invoice", frm.doc.document_name).then(docu => { 
                    frm.doc.party_type ="Customer";
                    frm.doc.party_name = docu.customer;
                    frm.trigger('party_name');
                    frm.doc.custom_service_value = docu.total;  
                    frm.doc.custom_tax = docu.total_taxes_and_charges;
                    frm.doc.custom_total = docu.grand_total;
                    frm.refresh_fields();
                });
            }
            else if(frm.doc.document_type == "Sales Order"){
                frappe.db.get_doc("Sales Order", frm.doc.document_name).then(docu => { 
                    frm.doc.party_type ="Customer";
                    frm.doc.party_name = docu.customer;
                    frm.trigger('party_name');
                    frm.doc.custom_service_value = docu.total;  
                    frm.doc.custom_tax = docu.total_taxes_and_charges;
                    frm.doc.custom_total = docu.grand_total;
                    frm.refresh_fields();
                    
                });
            }
            else if(frm.doc.document_type == "Quotation"){
                frappe.db.get_doc("Quotation", frm.doc.document_name).then(docu => { 
                    frm.doc.party_type ="Customer";
                    frm.doc.party_name = docu.customer;
                    frm.trigger('party_name');
                    frm.doc.custom_service_value = docu.total;  
                    frm.doc.custom_tax = docu.total_taxes_and_charges;
                    frm.doc.custom_total = docu.grand_total;
                    frm.refresh_fields();
                });
            }
    }
    },

    refresh(frm) {

    frm.set_query("custom_employee", function() {
    return {
        query: "bounya.queries.fetch_employee_with_role",
        filters: {
        }
    };
});
}

}); 

