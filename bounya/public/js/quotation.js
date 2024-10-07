frappe.ui.form.on('Quotation', {

    on_submit: function (frm) {
        frappe.call({
            method :"bounya.api.send_quotation_notification",
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
});