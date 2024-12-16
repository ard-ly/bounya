# Copyright (c) 2024, Omar Jaber and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CommitteeExtend(Document):
    def after_insert(self):
        allowed_users = frappe.db.sql_list("select parent from `tabHas Role` where role in ('General Manager', 'Chair Manager') and parenttype='User' and parent !='Administrator' group by parent")
        for allowed_user in allowed_users:
            if allowed_user:
                new_doc = frappe.new_doc("Notification Log")
                new_doc.from_user = frappe.session.user
                new_doc.for_user = allowed_user
                new_doc.type = "Share"
                new_doc.document_type = self.doctype
                new_doc.document_name = self.name
                new_doc.subject = "يوجد طلب تمديد لجنة جديد بحاجة للاعتماد."
                new_doc.insert(ignore_permissions=True)

                inbox_url = frappe.utils.data.get_url_to_form(self.doctype, self.name)
                mesg = "<p> You have a new Committee Extend,<br> please check the committee extend and submit<br> <b><a href='{0}'>Go to Committee Extend</a></b>".format(inbox_url)
                frappe.sendmail(
                  recipients=allowed_user,
                  subject="تمديد لجنة جديد",
                  message= mesg,
                  now=1,
                  retry=3
                )


    def on_submit(self):
        self.update_committee_dates()
        self.send_extend_notification()


    @frappe.whitelist()
    def update_committee_dates(self):
        frappe.db.sql("update `tabCommittees` set committee_from='{0}', committee_to='{1}' where name='{2}'".format(self.committee_extend_from, self.committee_extend_to, self.committee))
        frappe.db.commit()
        frappe.msgprint(_('Document updated successfully'), alert=True, indicator='green')
        

    @frappe.whitelist()
    def send_extend_notification(self):
        blocked_users = ['Administrator']
        hr_managers = frappe.get_all('Has Role', filters={'role': 'HR Manager', 'parenttype': 'User'}, fields=['parent'])
        
        hr_manager_emails = [
            manager['parent'] 
            for manager in hr_managers 
            if manager['parent'] not in blocked_users
        ]
        
        if hr_manager_emails:

            link = frappe.utils.get_url_to_form('Committees', self.committee)

            message = f"""
            <div style='direction: rtl; text-align: right;'>
                تم تمديد اللجنة <a href='{link}'>{self.committee}</a>:<br><br>
                <table border="1" class="text-center" style="border-collapse: collapse; width: 70%;">
                    <thead>
                        <tr>
                            <th width="20%"></th>
                            <th width="40%">من تاريخ</th>
                            <th width="40%">حتى تاريخ</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>السابق</th>
                            <td>{self.committee_from}</td>
                            <td>{self.committee_to}</td>
                        </tr>
                        <tr>
                            <th>الحالي</th>
                            <td>{self.committee_extend_from}</td>
                            <td>{self.committee_extend_to}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """

            subject = f"تمديد لجنة: {self.committee}"
            frappe.sendmail(
                recipients=hr_manager_emails,
                subject=subject,
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.committee,
                delayed=False
            )

