frappe.ui.form.on('Additional Salary', {
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

    // on_submit show dialog to view employee salary slip.
    on_submit: function (frm) {
        if(frm.doc.docstatus ==1){
            if (frm.doc.custom_employee_salary_slip){
                frappe.confirm('Do you want to view employee salary slip?',
                () => {
                    // action to perform if Yes is selected
                    console.log("YES");
                    frappe.open_in_new_tab = true; // This line in version 14
                    frappe.set_route("Form", "Salary Slip", frm.doc.custom_employee_salary_slip);
                }, () => {
                    // action to perform if No is selected
                    console.log("NO");
                });
         }
        }
    },

    after_cancel: function (frm) {
            frappe.call({
                method :"bounya.api.cancel_salary_slip_overwrite",
                args: {
                    doc_name:frm.doc.name,
                },
                callback:function(r){
                    if(r.message){
                        console.log(r.message);
                    }
                }
            });
    },

    // change query to shoe the statistical componenet
    set_component_query: function(frm) {
        if (!frm.doc.company) return;
        let filters = {company: frm.doc.company};
        if (frm.doc.type) {
            filters.type = "Erning";
        }
        frm.set_query("salary_component", function() {
            return {
                // filters: filters
            };
        });
    },

	custom_month(frm) {
		if (frm.doc.custom_month) {

			const d = new Date();
			let year = d.getFullYear();
            let month = frm.doc.custom_month
            var dateString = '' + year + '-' + month + '-' + '25';
			let payroll_date =  frappe.datetime.add_months(dateString, -1);
			frm.doc.payroll_date = new Date(payroll_date);
			frm.refresh_fields();
		}
	},

}); 

frappe.listview_settings["Additional Salary"] = {
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

        console.log(frappe.defaults.get_user_default("Payroll Month"))
        
        // let monthes = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' , 'October' , 'November' , 'December']
        let monthes = ['01' , '02' , '03' , '04' , '05' , '06' , '07' , '08' , '09' , '10' , '11' , '12' , '13']
        const today = new Date();
        let month = today.getMonth(); // returns from 0 to 11
        let month_str =  monthes[month];
        // frm.doc.custom_month = monthes[month];
        // frm.refresh_fields();
        // frm.trigger("custom_month")
        const d = new Date();
        let year = d.getFullYear();
        if(month_defulte){
            month_str = monthNames[month_defulte]
        }
        let end_date = '' + year + '-' + month_str + '-' +  '25';
        let payroll_date =  frappe.datetime.add_months(end_date, -1);
        frappe.route_options = {
            payroll_date:   payroll_date ,
            docstatus : ["!=" , 2]
        };
        console.log("sjldfffffffffffffff")
    },

};