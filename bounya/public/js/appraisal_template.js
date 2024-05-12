frappe.ui.form.on("Appraisal Template", {

});


frappe.ui.form.on("Appraisal Template Goal", {
    goals_remove:function(frm, cdt, cdn) {
        let highest_score_total = 0
        frm.doc.goals.forEach((row)=>{
            highest_score_total+= row.highest_score
        });
        frm.doc.goals.forEach((r)=>{
            r.per_weightage = (r.highest_score * 100)/highest_score_total;
            frm.refresh_fields("goals");
        });
    },
    highest_score:function(frm, cdt, cdn) {
        let highest_score_total = 0
        frm.doc.goals.forEach((row)=>{
            highest_score_total+= row.highest_score
        });
        frm.doc.goals.forEach((r)=>{
            r.per_weightage = (r.highest_score * 100)/highest_score_total;
            frm.refresh_fields("goals");
        });

    },


});