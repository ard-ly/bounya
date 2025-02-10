frappe.ui.form.on('Employee', {
    onload(frm) {
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
    },
    refresh(frm) {
        if(frm.doc.department){
            frm.set_query("custom_section", function() {
                return {
                    filters: [
                        ["Department","is_group", "=", 1],
                        ["Department","parent_department", "=", frm.doc.department]
                    ]
                }
            });
        }else{
            frm.set_query("custom_section", function() {
                return {
                    filters: [
                        ["Department","name", "=", 'null']
                    ]
                }
            });
        }


        if(frm.doc.custom_section){
            frm.set_query("custom_unit", function() {
                return {
                    filters: [
                        ["Department","is_group", "=", 0],
                        ["Department","parent_department", "=", frm.doc.custom_section]
                    ]
                }
            });
        }else{
            frm.set_query("custom_unit", function() {
                return {
                    filters: [
                        ["Department","name", "=", 'null']
                    ]
                }
            });
        }
    },
    department(frm) {
        frm.set_value("custom_section", '')
        frm.set_value("custom_unit", '')

        if(frm.doc.department){
            frm.set_query("custom_section", function() {
                return {
                    filters: [
                        ["Department","is_group", "=", 1],
                        ["Department","parent_department", "=", frm.doc.department]
                    ]
                }
            });
        }else{
            frm.set_query("custom_section", function() {
                return {
                    filters: [
                        ["Department","name", "=", 'null']
                    ]
                }
            });
        }
    },
    custom_section(frm) {
        frm.set_value("custom_unit", '')

        if(frm.doc.custom_section){
            frm.set_query("custom_unit", function() {
                return {
                    filters: [
                        ["Department","is_group", "=", 0],
                        ["Department","parent_department", "=", frm.doc.custom_section]
                    ]
                }
            });
        }else{
            frm.set_query("custom_unit", function() {
                return {
                    filters: [
                        ["Department","name", "=", 'null']
                    ]
                }
            });
        }
    },
    status(frm) {
        frm.set_value("custom_stop_resune",'')
    }
})