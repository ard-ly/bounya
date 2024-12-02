# Copyright (c) 2024, Omar Jaber and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class Committees(Document):
    def on_submit(self):
        self.send_reward_notification()
        self.change_committee_status()



    @frappe.whitelist()
    def get_employee_data(self, employee_name):
        emp = frappe.get_list("Employee", filters= {"name": employee_name}, fields = ["*"])[0]
        return emp


    @frappe.whitelist()
    def change_committee_status(self):
        current_date = getdate(nowdate())
        start_date = getdate(self.committee_from)
        end_date = getdate(self.committee_to)

        if start_date <= current_date <= end_date:
            self.committee_status = 'Active'
        else:
            self.committee_status = 'Outdated'




    @frappe.whitelist()
    def send_reward_notification(self):
        blocked_users = ['Administrator']
        hr_managers = frappe.get_all('Has Role', filters={'role': 'HR Manager', 'parenttype': 'User'}, fields=['parent'])
        
        hr_manager_emails = [
            manager['parent']
            for manager in hr_managers 
            if manager['parent'] not in blocked_users
        ]
        
        reward_exists = any(item.reward for item in self.get('committee_members'))

        if hr_manager_emails and reward_exists:

            link = frappe.utils.get_url_to_form(self.doctype, self.name)

            table_rows = ''
            for item in self.get('committee_members'):
                table_rows += f"""
                <tr>
                    <td>{item.idx}</td>
                    <td>{item.member_name}</td>
                    <td>{item.designation}</td>
                    <td>{item.email}</td>
                    <td>{item.phone_number}</td>
                </tr>
                """

            message = f"""
            <div style='direction: rtl; text-align: right;'>
                تم تشكيل لجنة جديدة <a href='{link}'>{self.name}</a> وتحتوي على مكافأة للأعضاء التاليين:<br><br>
                <table border="1" class="text-center" style="border-collapse: collapse; width: 70%;">
                    <thead>
                        <tr>
                            <th width="3%">م</th>
                            <th width="25%">اسم العضو</th>
                            <th width="25%">المسمى الوظيفي</th>
                            <th width="25%">البريد الإلكتروني</th>
                            <th width="25%">رقم الهاتف</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            """

            subject = f"تشكيل لجنة جديدة: {self.name}"
            frappe.sendmail(
                recipients=hr_manager_emails,
                subject=subject,
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.name,
                delayed=False
            )



