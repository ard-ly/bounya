frappe.ui.form.on('Payroll Entry', {
    setup: function (frm) {
        let monthes = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' , 'October' , 'November' , 'December']
		if (frm.is_new()) {
			const today = new Date();
			let month = today.getMonth(); // returns from 0 to 11
			frm.doc.custom_month = monthes[month];
			frm.refresh_fields();
            frm.trigger("custom_month")
	}
	},
	custom_month(frm) {
		if (frm.doc.custom_month) {

			const d = new Date();
			let year = d.getFullYear();
            let month = frm.doc.custom_month
            var dateString = '' + year + '-' + month + '-' + '25';
			let payroll_date =  frappe.datetime.add_months(dateString, -1);
			frm.doc.start_date = new Date(payroll_date);
			frm.refresh_fields();
		}
	},

	refresh:function (frm) {
		if (
			!frm.doc.salary_slips_submitted ||
			(frm.doc.__onload && frm.doc.__onload.submitted_ss)
		) {
		frappe.call({
			method: "hrms.payroll.doctype.payroll_entry.payroll_entry.payroll_entry_has_bank_entries",
			args: {
				name: frm.doc.name,
				payroll_payable_account: frm.doc.payroll_payable_account,
			},
			callback: function (r) {
				if (r.message && !r.message.submitted) {
					frm.add_custom_button(__('Recalculate Salary values'), function (){
						recalculate_salary_slip(frm);
					});
				}
			},
		});
	}
    },

}); 
let recalculate_salary_slip = function (frm) {
	frappe.call({
		method: "bounya.api.recalculate_salary_slip",
		args: {
			doc: frm.doc.name,
		},
		callback: function (r) {
			if (r.message) {
				frappe.msgprint(__("Item got created successfully!"));
				frappe.msgprint(r.message);
			}
		},
	});

};