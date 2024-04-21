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

	// custom_additional_salary_type: function(frm) {
    //     if (frm.doc.custom_additional_salary_type){
    //         frappe.call({
    //             method: "bounya.override.additional_salary.fetch_addetionl_fraction",
    //             args: {
    //                 "additionl_type": frm.doc.custom_additional_salary_type,
    //             },
    //             callback: function (r) {
    //                 if (r.message){
    //                     frm.set_value("custom_additional_fraction" , r.message)
    //                     frm.refresh_field("custom_additional_fraction")

    //                 }
    //             }
    //         })
    //     }
    //     if (frm.doc.custom_total_additional_hours && frm.doc.custom_base_amount && frm.doc.custom_additional_fraction ) {
    //         frm.set_value("amount" , (frm.doc.custom_total_additional_hours * frm.doc.custom_additional_fraction * frm.doc.custom_base_amount))
    //         frm.refresh_field("amount")
    //     }    },  
    // custom_calculate_from_work_hours:function (frm) {
    //     if (frm.doc.custom_calculate_from_work_hours){
    //         frappe.call({
    //             method: "bounya.override.additional_salary.fetch_addetionl_component",
    //             args: {
    //             },
    //             callback: function (r) {
    //                 if (r.message){
    //                     frm.set_value("salary_component" , r.message)
    //                     frm.refresh_field("salary_component")

    //                 }
    //             }
    //         })
    //     }      
    // },

    // payroll_date: function(frm) {
    //     frm.trigger("fetch_hour_cost")
    // },

    // employee: function(frm) {
    //     frm.trigger("fetch_hour_cost")
    // },

    // custom_total_additional_hours: function(frm) {
    //     if (frm.doc.custom_total_additional_hours && frm.doc.custom_base_amount && frm.doc.custom_additional_fraction ) {
    //         frm.set_value("amount" , (frm.doc.custom_total_additional_hours * frm.doc.custom_additional_fraction * frm.doc.custom_base_amount))
    //         frm.refresh_field("amount")
    //     }
        
    // },


    // fetch_hour_cost : function(frm) {
    //     if( frm.doc.employee && frm.doc.payroll_date){
    //         frappe.call({
    //             method: "bounya.override.additional_salary.check_sal_struct",
    //             args: {
    //                 "employee": frm.doc.employee,
    //                 "date": frm.doc.payroll_date
    //             },
    //             callback: function (r) {
    //                 if (r.message){
    //                     frm.set_value("custom_base_amount" , r.message)
    //                     frm.refresh_field("custom_base_amount")

    //                 }
    //             }
    //         })
    //     }
    //     if (frm.doc.custom_total_additional_hours && frm.doc.custom_base_amount && frm.doc.custom_additional_fraction ) {
    //         frm.set_value("amount" , (frm.doc.custom_total_additional_hours * frm.doc.custom_additional_fraction * frm.doc.custom_base_amount))
    //         frm.refresh_field("amount")
    //     }
    // },
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