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
}); 