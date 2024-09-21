frappe.ui.form.on('Lead', {

    onload: function (frm) {},

    // custom_qualification_template:function (frm) {
    //     if (frm.doc.custom_qualification_template){
    //         frm.clear_table("custom_qualification_grade_table");
    //         // frm.save();
    //         // frm.refresh();
    //         frappe.call({
    //             method :"bounya.api.get_qualification",
    //             args: {
    //                 doc:frm.doc.name,
    //                 qualification_template: frm.doc.custom_qualification_template,
    //             },
    //             callback:function(r){
    //                 if(r.message){
    //                     frm.refresh_field("custom_qualification_grade_table");
    //                     console.log(r.message);
    //                     // window.location.reload();
    //                 }
    //             }
    //         });
    //     }
    // },
    // custom_qualification_grade_table:function (frm) {
    //     frappe.call({
	// 		method :"bounya.api.",
	// 		args: {
    //             doc:frm.doc,
    //         },
	// 		callback:function(r){
	// 			if(r.message){
	// 				console.log(r.message);
	// 			}
	// 		}
	// 	});
    // },
});