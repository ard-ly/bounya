# Copyright (c) 2024, Omar Jaber and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CommitteeExtend(Document):
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

