// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mail Import', {
	mail_type: function(frm) {
		frm.set_value("output", )		
	},
	download_template: function(frm) {
		if(frm.doc.mail_type=='Incoming Mail'){
			window.location.href = '/assets/bounya/file/incoming_mail.csv';
		}else{
			window.location.href = '/assets/bounya/file/outgoing_mail.csv';
		}
	},
	attach_file: function (frm) {
    	frm.set_value("output", )
    },
    get_data: function (frm) {
    	if(frm.doc.attach_file && frm.doc.mail_type){

            frappe.call({
		        doc: cur_frm.doc,
		        method: "import_mail_data",
		        callback: function(r) {
		        	frm.set_value('output', r.message)
		            cur_frm.refresh_fields(['output']);
		        }
		    });
	    }else{
	    	frappe.throw("Please attach a file first.")
	    }
    }
});
