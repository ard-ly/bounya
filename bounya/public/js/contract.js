frappe.ui.form.on('Contract', {
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
}); 