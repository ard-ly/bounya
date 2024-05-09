frappe.ui.form.on('Loan Application', {

    applicant(frm) {
        if (frm.doc.applicant){
        frappe.call({
            method: "bounya.api.get_last_loans",
            args: {
                applicant_type : frm.doc.applicant_type,
                applicant: frm.doc.applicant,
            },
            frm: frm,
            callback: r => {
                if (r.message){
                    if(r.message.applicant_dependent){
                        frm.doc.custom_applicant_dependent = r.message.applicant_dependent;
                    }
                    // Employee Advance.
                    if (r.message.last_ea && r.message.last_ea !="" && r.message.last_ea != null){
                        frm.doc.custom_employee_advance = r.message.last_ea.name;
                        frm.doc.custom_employee_advance_date = r.message.last_ea.posting_date;
                        frm.doc.custom_employee_advance_reasons = r.message.last_ea.purpose;
                    }
                    // Last Loan(not type Solidarity Fund or Treatment).
                    if(r.message.last_loan && r.message.last_loan !="" && r.message.last_loan != null){
                        frm.doc.custom_last_loan_link = r.message.last_loan.name ;
                        frm.doc.custom_last_loan_type = r.message.last_loan.loan_type ;
                        frm.doc.custom_last_loan_date = r.message.last_loan.posting_date ;
                        frm.doc.custom_last_loan_company = r.message.last_loan.company;
                        if (r.message.last_loan_reasons){
                            frm.doc.custom_last_loan_reasons = r.message.last_loan_reasons;
                        }
                    }

                    // Last Solidarity Fund Loan.
                    if(r.message.last_sf && r.message.last_sf !="" && r.message.last_sf != null){
                        frm.doc.custom_solidarity_fund_loan_link = r.message.last_sf.name;
                        frm.doc.custom_solidarity_fund_loan_type = r.message.last_sf.loan_type ;
                        frm.doc.custom_solidarity_fund_loan_date = r.message.last_sf.posting_date ;
                        if (r.message.last_sf_reasons){
                            frm.doc.custom_solidarity_fund_loan_reasons = r.message.last_sf_reasons ;
                        }
                    }

                    // Last Treatment Loan.
                    if(r.message.last_treatment && r.message.last_treatment !="" && r.message.last_treatment != null){
                        frm.doc.custom_treatment_loan_link = r.message.last_treatment.name;
                        frm.doc.custom_treatment_loan_type = r.message.last_treatment.loan_type ;
                        frm.doc.custom_treatment_loan_date = r.message.last_treatment.posting_date ;
                        frm.doc.custom_treatment_loan_amount = r.message.last_treatment.loan_amount ;
                        if (r.message.last_treatment_reasons){
                            frm.doc.custom_treatment_loan_reasons = r.message.last_treatment_reasons ;
                        }
                    }  
                    frm.refresh_fields();
                }
            }
        })
    }
},
}); 