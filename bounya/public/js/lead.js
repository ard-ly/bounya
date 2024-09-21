frappe.ui.form.on('Lead', {

    validate: function (frm) {
        if(frm.doc.custom_minimum_qualification_score > 0){
            if(frm.doc.custom_total_grades < frm.doc.custom_minimum_qualification_score){
                frm.doc.qualification_status = "Unqualified";
            }
            else{
                frm.doc.qualification_status = "Qualified";
            }
        }
    },

    custom_qualification_template:function (frm) {
        if (frm.doc.custom_qualification_template){
            // frm.clear_table("custom_qualification_grade_table");
            frm.set_value('custom_qualification_grade_table', []);
            frappe.call({
                method :"bounya.api.get_qualification",
                args: {
                    qualification_template: frm.doc.custom_qualification_template,
                },
                callback:function(r){
                    if(r.message){
                        console.log(r.message.q_list);

                        r.message.q_list.forEach((row)=>{
                            var child = frm.add_child('custom_qualification_grade_table');
                            child.qualification = row;
                            child.grade = 0;
                        });

                        frm.refresh_fields();
                    }
                }
            });
        }
    },
});

frappe.ui.form.on('Qualification Grade Table', {
    grade: function(frm, cdt, cdn) {
        let grade_sum = 0
        frm.doc.custom_qualification_grade_table.forEach((row)=>{
            grade_sum += row.grade
        });
        frm.doc.custom_total_grades = grade_sum;
        frm.refresh_fields();
    },

    custom_qualification_grade_table_remove:function(frm, cdt, cdn) {
        let grade_sum = 0
        frm.doc.custom_qualification_grade_table.forEach((row)=>{
            grade_sum += row.grade
        });
        frm.doc.custom_total_grades = grade_sum;
        frm.refresh_fields();
    },
});