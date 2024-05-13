frappe.ui.form.on('Salary Slip', {
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
    // employee:function (frm) {
    //     frappe.call({
    //         method: "bounya.override.py.salary_slip.check_sal_struct",
    //         args: {
    //             "grade": frm.doc.grade,
    //             "marbot": frm.doc.custom_dependent
    //         },
    //         callback: function (r) {
    //             if (r.message){
    //                 frm.set_value("base" , r.message)
    //                 frm.refresh_field("base")

    //             }
    //         }
    //     })
    // }
});

frappe.listview_settings["Salary Slip"] = {
    // hide_name_column: true,
    // add_fields: ["company", "is_default"],

          
    onload: function (me) {
        console.log(frappe.defaults.get_user_default("Payroll Month"))
        let month_defulte = frappe.defaults.get_user_default("Payroll Month")
        console.log(month_defulte)
        const monthNames = {
            January: '01',
            February: '02',
            March: '03',
            April: '04',
            May: '05',
            June: '06',
            July: '07',
            August: '08',
            September: '09',
            October: '10',
            November: '11',
            December: '12'
          };
        console.log(monthNames[month_defulte])

        let monthes = ['01' , '02' , '03' , '04' , '05' , '06' , '07' , '08' , '09' , '10' , '11' , '12' , '13']
        const today = new Date();
        let month = today.getMonth(); // returns from 0 to 11
        let month_str =  monthes[month];
        if(month_defulte){
            month_str = monthNames[month_defulte]
        }
        const d = new Date();
        let year = d.getFullYear();
        var end_date = '' + year + '-' + month_str + '-' +  '25';
        let start_date =  frappe.datetime.add_months(end_date, -1);
        frappe.route_options = {
            start_date:   start_date ,
            docstatus : ["!=" , 2]
        };
    },
};
