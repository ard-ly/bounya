frappe.ui.form.on("Employee", "onload", function(frm){
    frm.set_query("custom_employee_bank_branch", function(){
        return {
            query: "bounya.api.fetch_bank_branch_list",
            filters: {
              bank_name: frm.doc.custom_bank_name,
            },
          };
    });

    frm.set_query("custom_office", function(){
      return {
          query: "bounya.api.fetch_branchs_office_list",
          filters: {
          branch: frm.doc.branch,
          },
        };
  });
});    
  
// frappe.ui.form.on('Employee', {
//   // frm passed as the first parameter
//   setup(frm) {
//       frm.doc.employee_number = 88888888888
//       frm.refresh_fields();
//   },

// })
