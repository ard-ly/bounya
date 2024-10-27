frappe.ui.form.on('Sales Order', {

    refresh: function (frm) {
        if (frm.doc.docstatus  == 1){
			frm.add_custom_button(__('Contract'), 
            function () {
				frappe.model.open_mapped_doc({
					method: "bounya.api.create_contract_from_so",
					frm: frm,
				})
			},__("Create"));

			if (frappe.user.has_role("Tower Management")){
				if (frm.doc.custom_contract != null ){
					// && frm.doc.order_type == "Equipment Installation"
					frm.add_custom_button(__('Equipment Installation'), 
					function () {
						frappe.model.open_mapped_doc({
							method: "bounya.api.create_equipment_installation_from_so",
							frm: frm,
						})
					},__("Create"));
				
				}
			}
			
	    }
    },

	onload: function(frm) {
		frm.set_query("custom_realty_name", function() {
			return {
				query: "bounya.queries.filter_realty",
				filters: {}
			};
		});
	},

	on_submit: function (frm) {
        frappe.call({
            method :"bounya.api.send_so_notification",
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