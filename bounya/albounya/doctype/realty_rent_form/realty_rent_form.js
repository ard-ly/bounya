// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Realty Rent Form', {
    user(frm) {
        if(frm.doc.user){
            frappe.model.get_value('Customer', {'custom_user': frm.doc.user}, 'name',
              function(d) {
                frm.set_value("customer", d.name)
              })
        }
    }
});

frappe.ui.form.on("Realty Rent Form", "refresh", function(frm) {
    frm.fields_dict['realty_rent_table'].grid.get_field('realty').get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        return{ 
            filters:[
                    ['realty_type', '=', child.realty_type],
                    ['docstatus', '=', 1]
                ]
        }
    }
});
