
frappe.ui.form.on('Salary Structure', {
	// refresh: function(frm) {
    //     frm.add_custom_button(__("Test Salary Slip"), function() {
    //         frm.trigger("open_salary_slip2");
    //     }, __("Actions"));
	// },

// old calculations (Hadeel)

	// refresh: function(frm) {
    //     frm.add_custom_button(__("Calculate Base Salary Slip"), function() {
    //         frm.trigger("full_samples_table");
    //     }, __("Actions"));
	// },
    // full_samples_table : function(frm) {
    //     cur_frm.clear_table("custom_samples_table");
    //     frm.refresh_field("custom_samples_table"); 

    //     cur_frm.clear_table("custom_sample_table_married");
    //     frm.refresh_field("custom_sample_table_married"); 

    //     cur_frm.clear_table("custom_sample_table_married_with_child");
    //     frm.refresh_field("custom_sample_table_married_with_child"); 

    //     cur_frm.clear_table("custom_sample_table_single_hassan");
    //     frm.refresh_field("custom_sample_table_single_hassan"); 
      
    //     cur_frm.clear_table("custom_sample_table_single_high");
    //     frm.refresh_field("custom_sample_table_single_high");       

    //     cur_frm.clear_table("custom_sample_table_married_hassan");
    //     frm.refresh_field("custom_sample_table_married_hassan"); 
   
    //     cur_frm.clear_table("custom_sample_table_married_high");
    //     frm.refresh_field("custom_sample_table_married_high"); 
           
    //     cur_frm.clear_table("custom_sample_table_married_with_child_hassan");
    //     frm.refresh_field("custom_sample_table_married_with_child_hassan"); 
           
    //     cur_frm.clear_table("custom_sample_table_married_with_child_high");
    //     frm.refresh_field("custom_sample_table_married_with_child_high"); 
        
    //     var min = frm.doc.custom_min_salary 
    //     var max = frm.doc.custom_max_salary 
    //     var length = 50
    //     var step = (max - min )/ (length -1)
    //     var bases = []
    //     bases = Array.from({ length }, (_, i) => min + i * step);
    //     bases.sort()
    //     console.log(bases)
    //     // Single week sample
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Single',
    //                 number_of_children : 0,
    //                 base : b,
    //                 evaluation : "Weak",
    //                 performance_factor : 0.0 
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Single" , "custom_samples_table");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_samples_table");
    //             },
    //         });
    //     })
    //     // refresh_field("custom_samples_table");
    //     // Single Hassan Sample
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Single',
    //                 number_of_children : 0,
    //                 base : b,
    //                 evaluation : "Hassan",
    //                 performance_factor : 0.2
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Single Hassan" , "custom_sample_table_single_hassan");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_single_hassan");
    //             },
    //         });
    //     })
    //     // refresh_field("custom_sample_table_single_hassan");

    //     // single High
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Single',
    //                 number_of_children : 0,
    //                 base : b,
    //                 evaluation : "high",
    //                 performance_factor : 0.3
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Single High" , "custom_sample_table_single_high");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_single_high");
    //             },
    //         });
    //     })
        
    //     // Married 0 child weak 
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Married',
    //                 number_of_children : 0,
    //                 base : b,
    //                 evaluation : "Weak",
    //                 performance_factor : 0.0 
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Married" , "custom_sample_table_married");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_married");
    //             },
    //         });
    // })
    // // refresh_field("custom_sample_table_married");

    //     // Married 0 child Hassan 
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Married',
    //                 number_of_children : 0,
    //                 base : b,
    //                 evaluation : "Hassan",
    //                 performance_factor : 0.2
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Married Hassan" , "custom_sample_table_married_hassan");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_married_hassan");
    //             },
    //         });
    //     })

    //         // Married 0 child high 
    //         bases.forEach((b) =>{
    //             frappe.call({
    //                 method: 'bounya.api.make_demo_data',
    //                 args: {
    //                     doc : frm.doc , 
    //                     salary_structure :frm.doc.name,
    //                     marital_status : 'Married',
    //                     number_of_children : 0,
    //                     base : b,
    //                     evaluation : "high",
    //                     performance_factor : 0.3
    //                 },
    //                 callback: function(r) {
    //                         // code snippet
    //                     var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Married High" , "custom_sample_table_married_high");
    //                     new_child_row.base_salary = r.message[0]
    //                     new_child_row.net_salary = r.message[1]
    //                     refresh_field("custom_sample_table_married_high");
    //                 },
    //             });
    //       })
    
    //     // Marred with child week
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Married',
    //                 number_of_children : 1,
    //                 base : b,
    //                 evaluation : "Weak",
    //                 performance_factor : 0.0 
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Married with Child" , "custom_sample_table_married_with_child");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_married_with_child");
    //             },
    //         });
    //     })

    //     // Marred with child Hassan
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Married',
    //                 number_of_children : 1,
    //                 base : b,
    //                 evaluation : "Hassan",
    //                 performance_factor : 0.2 
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Married with Child Hassan" , "custom_sample_table_married_with_child_hassan");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_married_with_child_hassan");
    //             },
    //         });
    //     })

    //     // Marred with child High
    //     bases.forEach((b) =>{
    //         frappe.call({
    //             method: 'bounya.api.make_demo_data',
    //             args: {
    //                 doc : frm.doc , 
    //                 salary_structure :frm.doc.name,
    //                 marital_status : 'Married',
    //                 number_of_children : 1,
    //                 base : b,
    //                 evaluation : "high",
    //                 performance_factor : 0.3 
    //             },
    //             callback: function(r) {
    //                     // code snippet
    //                 var new_child_row = frappe.model.add_child(frm.doc, "Sample Table Married with Child High" , "custom_sample_table_married_with_child_high");
    //                 new_child_row.base_salary = r.message[0]
    //                 new_child_row.net_salary = r.message[1]
    //                 refresh_field("custom_sample_table_married_with_child_high");
    //             },
    //         });
    //     })
    // }
    
    });