
frappe.ui.form.on('Supplier', {
    refresh(frm) {

        frm.set_query('custom__default_company_bank_account', () => {
            return {
                filters: {
                    is_company_account: false
                }
            }
        })
    }

})