// frappe.ui.form.on('Salary Slip', {
// 	refresh(frm) {
// 		// your code here
//         frm.set_value('start_date', '2024-01-01')
// 	},

// })
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
