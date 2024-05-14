// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

let rate = 100
frappe.ui.form.on("Appraisal", {
    // refresh(frm) {
    //     frappe.msgprint(__(" 555555555555"));
    // },
	calculate_total(frm) {
		let total = 0;

		frm.doc.goals.forEach((d) => {
			total += flt(d.custom_highest_score);
		});

		frm.set_value("total_score", total);
	},
    appraisal_template: function(frm){
        frappe.db.get_doc('Appraisal Template', frm.doc.appraisal_template).then(doc => {
            rate = doc.rate_from
        });
        frm.trigger('get_highest_scores');

    },
    get_highest_scores:function(frm){
           frappe.call({
                method:"bounya.override.py.appraisal.get_highest_scores",
                args:{template : frm.doc.appraisal_template},
                callback:(r)=>{
                        let scores = r.message
                        for(let i =0 ; i<scores.length;++i){
                            frm.doc.goals[i].custom_highest_score = scores[i];
                        }
                       frm.refresh_fields();
                }
           });
    },
});


frappe.ui.form.on("Appraisal Goal", {
	score(frm, cdt, cdn) {

		let d = frappe.get_doc(cdt, cdn);

		if (flt(d.score) > 5) {
			// frappe.msgprint(__("Score must be less than or equal to 555555555555"));
			d.score = 0;
			refresh_field("score", d.name, "goals");
		} else {
			frm.trigger("set_score_earned", cdt, cdn);
		}
	},

	per_weightage(frm, cdt, cdn) {
		frm.trigger("set_score_earned", cdt, cdn);
	},

	goals_remove(frm, cdt, cdn) {
		frm.trigger("set_score_earned", cdt, cdn);
	},

	set_score_earned(frm, cdt, cdn) {
		let d = frappe.get_doc(cdt, cdn);

		score_earned = flt(d.new_score);
		frappe.model.set_value(cdt, cdn, "score_earned", score_earned);

		frm.trigger("calculate_total");
	}
});