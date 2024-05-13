
frappe.ui.form.on("Appraisal", {
    // refresh(frm) {
    //     frappe.msgprint(__(" 555555555555"));
    // },
	calculate_total(frm) {
		let total = 0;

		frm.doc.goals.forEach((d) => {
			total += flt(d.score_earned  / 5 * 100);
		});

		frm.set_value("total_score", total);
	}
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

		let score_earned = flt(d.score) * flt(d.per_weightage) / 100;
		frappe.model.set_value(cdt, cdn, "score_earned", score_earned);

		frm.trigger("calculate_total");
	}
});