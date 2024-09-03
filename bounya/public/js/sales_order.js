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
	    }
    },

	onload: function(frm) {
		let types = ['Sales','Maintenance','Shopping Cart','Towers'];
        frm.set_df_property("order_type", "options", types);
        frm.refresh_field("order_type");
	},
});