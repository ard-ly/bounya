// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("New Item Request", {
  refresh: function (frm) {
    if (frm.doc.status == "Approved")
      frm.add_custom_button(__(__("Create Item")), () => {
        frm.call({
          doc: frm.doc,
          method: "create_item",
          args: {
            item_name: frm.doc.item_name,
            item_category: frm.doc.item_category,
            description: frm.doc.description,
            expense_account: frm.doc.default_expense_account,
            income_account: frm.doc.default_income_account,
          },
          callback: (r) => {
            // on success
            if (r.message)
              frappe.msgprint(__("Item got created successfully!"));
            else frappe.msgprint(__("Item is not created!"));
          },
        });
      });
  },
});
