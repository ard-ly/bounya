frappe.ui.form.on("Employee", "onload", function(frm){
    frm.set_query("custom_employee_bank_branch", function(){
        return {
            query: "bounya.api.fetch_bank_branch_list",
            filters: {
              bank_name: frm.doc.custom_bank_name,
            },
          };
    });
});    

