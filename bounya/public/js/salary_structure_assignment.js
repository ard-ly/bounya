frappe.ui.form.on('Salary Structure Assignment', {
	// refresh: function(frm) {
    //     frm.add_custom_button(__("Test Salary Slip"), function() {
    //         frm.trigger("open_salary_slip2");
    //     }, __("Actions"));
	// },
	// custom_net_salary: function(frm) {

    //     frm.trigger("calculate_incremment_value")
    // },    

    // custom_supervisory:function(frm) {

    //     frm.trigger("calculate_incremment_value")

    // },
    // custom_reward:function(frm) {

    //     frm.trigger("calculate_incremment_value")

    // },
    // custom_leadership:function(frm) {

    //     frm.trigger("calculate_incremment_value")

    // },
    // custom_risk:function(frm) {

    //     frm.trigger("calculate_incremment_value")

    // },
    // custom_performance_factor:function(frm) {

    //     frm.trigger("calculate_incremment_value")

    // },
    
    // custom_housing_allowance:function(frm) {

    //     frm.trigger("calculate_incremment_value")

    // },
    
    // // 90:00
    custom_evaluation : function(frm) {
        frm.set_value('custom_performance_factor_' , 0.0)
        if (frm.doc.custom_evaluation == 'Good') {
            frm.set_value('custom_performance_factor_' , 0.15)
        }
        if (frm.doc.custom_evaluation == 'Hassan') {
            frm.set_value('custom_performance_factor_' , 0.2)
        }
        if (frm.doc.custom_evaluation == 'high') {
            frm.set_value('custom_performance_factor_' , 0.3)
        }
    },
    // custom_marital_status: function(frm) {
    //     if (frm.doc.custom_marital_status=='Single'){
    //         // frm.set_value("custom_family_allowance" , 0)
    //         frm.set_value("custom_housing_allowance" , 100)
    //     }
    //     else if (frm.doc.custom_marital_status=='Married' && frm.doc.custom_number_of_children == 0 ){
    //         // frm.set_value("custom_family_allowance" , 100)
    //         frm.set_value("custom_housing_allowance" , 150)
    //     }
    //     else if (frm.doc.custom_marital_status=='Married' && frm.doc.custom_number_of_children != 0 ){
    //         // frm.set_value("custom_family_allowance" , 200)
    //         frm.set_value("custom_housing_allowance" , 200)
    //     }
    //     else{
    //         // frm.set_value("custom_family_allowance" , 0)
    //         frm.set_value("custom_housing_allowance" , 0)
    //     }
    //     frm.set_value("custom_family_allowance" , 0)
    //     frm.refresh_field("custom_family_allowance")
    //     frm.refresh_field("custom_housing_allowance")
    //     frm.trigger("calculate_incremment_value")
    // },


    // hadeel

// move base salary to salary slip
    // grade: function(frm){
    //     if (frm.doc.grade){
    //         frappe.call({
    //             method: "bounya.api.fetch_base_from_slip",
    //             args: {
    //                 "grade": frm.doc.grade,
    //                 "marbot": frm.doc.custom_dependent
    //             },
    //             callback: function (r) {
    //                 if (r.message){
    //                     frm.set_value("base" , r.message)
    //                     frm.refresh_field("base")

    //                 }
    //             }
    //         })
    //     }

    // },




    // salary_structure:function(frm){
    //     frm.trigger("grade")
    // },
//     calculate_incremment_value(frm){
//         pass
//         // const family_allowance = frm.doc.custom_family_allowance 
//         // const housing_allowance = frm.doc.custom_housing_allowance

//         // if (frm.doc.custom_net_salary){
//         //     var TT = 0
//         //     if (frm.doc.custom_marital_status == "Single"){
//         //         TT = 150
//         //     }
//         //     else if (frm.doc.custom_marital_status == "Married"){
//         //         TT = 200 + 25 * frm.doc.custom_number_of_children
//         //     }
//         //     else{
//         //         TT = 150
//         //     }
//         //     console.log(TT)
//         //     var supervisory = frm.doc.custom_net_salary * frm.doc.custom_supervisory
//         //     var leadership = frm.doc.custom_net_salary * frm.doc.custom_leadership
//         //     // var performance = (frm.doc.custom_net_salary +  housing_allowance + family_allowance + frm.doc.custom_transport +  supervisory + leadership ) * frm.doc.custom_performance_factor
//         //     var performance = (frm.doc.custom_net_salary +  housing_allowance + family_allowance +  supervisory + leadership ) * frm.doc.custom_performance_factor
//         //     var reward = frm.doc.custom_reward
//         //     var risk = (frm.doc.custom_net_salary +  housing_allowance  ) * frm.doc.custom_risk
//         //     var total_net = frm.doc.custom_net_salary + family_allowance + housing_allowance + supervisory + leadership + performance + reward + risk

//         //     // توزيع حد الاعفاء بين مكونات الراتب الأساسية الداخلة في عملية الترفيع
//         //     // Tb ==> T base ,  Th ==> T housing  , Tf ==> T Family

//         //     var Tb =  (frm.doc.custom_net_salary / total_net) * TT 
//         //     var Th =  (housing_allowance / total_net) * TT 
//         //     var Tf =  (family_allowance / total_net) * TT 
//         //     var TR =  (reward / total_net) * TT 

//         //     var b50 = (frm.doc.custom_net_salary / total_net) * 50
//         //     var H50 = (housing_allowance / total_net) * 50
//         //     var F50 = (family_allowance / total_net) * 50
//         //     var R50 = (reward / total_net) * 50
//         //     if (total_net > 1000){
                
//         //         var increased_base = (frm.doc.custom_net_salary - 0.1 * Tb - b50 ) / 0.8167125
//         //         var increased_housing_allowance = (housing_allowance  - 0.1 * Th - H50) / 0.8167125
//         //         var increased_family_allowance = (family_allowance - 0.1 * Tf - F50 ) / 0.8613
//         //         var increased_reward = (reward - 0.1 * TR - R50 ) / 0.8167125

//         //     }
//         //     else{
//         //         var increased_base = (frm.doc.custom_net_salary - 0.05 * Tb  ) / 0.86365
//         //         var increased_housing_allowance = (housing_allowance  - 0.05 * Th ) / 0.86365
//         //         var increased_family_allowance = (family_allowance - 0.05 * Tf  ) / 0.86365
//         //         var increased_reward = (reward - 0.05 * TR  ) / 0.86365
//         //     }


//         //     frm.set_value('base' , increased_base)
//         //     frm.set_value('custom_increased_housing_allowance' , increased_housing_allowance)
//         //     frm.set_value('custom_increased_family_allowance' , increased_family_allowance)
//         //     frm.set_value('custom_increased_reward' , increased_reward)
//         //     frm.refresh_field("base")
//         //     frm.refresh_field("custom_increased_housing_allowance")
//         //     frm.refresh_field("custom_increased_family_allowance")
//         //     frm.refresh_field("frm.doc.custom_increased_reward")
//         // }
        
//     },
//     // validat: function(frm) {
//     //     frm.trigger("calculate_incremment_value")
//     // },
});



frappe.listview_settings["Salary Structure Assignment"] = {
    // hide_name_column: true,
    // add_fields: ["company", "is_default"],

          
    onload: function (me) {
        frappe.route_options = {
            docstatus : ["!=" , 2]
        };
    },

};