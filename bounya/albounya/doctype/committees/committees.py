# Copyright (c) 2024, Omar Jaber and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class Committees(Document):
    def on_submit(self):
        if not self.email_sent:
            self.send_reward_notification()
        self.change_committee_status()
        self.add_committee_in_employee()
        # self.add_custom_user_permission()


    def on_cancel(self):
        employee_committees = frappe.get_all('Employee Committees',filters={'committee_name': self.name},fields=['name'])
        for record in employee_committees:
            frappe.delete_doc('Employee Committees', record['name'])


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
    def add_committee_in_employee(self):
        current_date = getdate(nowdate())
        start_date = getdate(self.committee_from)
        end_date = getdate(self.committee_to)

        for prosecutor in self.committee_table:
            status = ''
            if prosecutor.employee:
                if not frappe.db.exists("Employee Committees", {"committee_name": self.name, "parent": prosecutor.employee}):
                    doc = frappe.get_doc("Employee", prosecutor.employee)

                    if start_date <= current_date <= end_date:
                        status = 'Active'
                    else:
                        status = 'Outdated'

                    doc.append('custom_employee_committees', {
                        "committee_name": self.name,
                        "committee_status": status
                    })
                    doc.flags.ignore_mandatory = True
                    doc.save(ignore_permissions=True)


    @frappe.whitelist()
    def add_custom_user_permission(self):
        for member in self.committee_table:
            if member.from_system:
                member_email = frappe.get_value("Employee", filters = {"name": member.employee}, fieldname = "user_id") or None

                if member_email and not frappe.db.exists("Custom User Permission", {"applicable_for": 'Committees', "document": self.name, "user": member_email}):
                    frappe.get_doc({
                        "doctype":"Custom User Permission",
                        "applicable_for": 'Committees',
                        "document": self.name,
                        "user": member_email
                    }).insert(ignore_permissions=True)



    @frappe.whitelist()
    def send_reward_notification(self):
        blocked_users = ['Administrator']
        hr_managers = frappe.get_all('Has Role', filters={'role': 'HR Manager', 'parenttype': 'User'}, fields=['parent'])
        
        hr_manager_emails = [
            manager['parent'] 
            for manager in hr_managers 
            if manager['parent'] not in blocked_users
        ]
        
        reward_exists = any(item.reward for item in self.get('committee_table'))

        if hr_manager_emails and reward_exists:

            link = frappe.utils.get_url_to_form(self.doctype, self.name)

            table_rows = ''
            for item in self.get('committee_table'):
                table_rows += f"""
                <tr>
                    <td>{item.idx}</td>
                    <td>{item.member_name}</td>
                    <td>{item.designation}</td>
                    <td>{item.adjective}</td>
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
                            <th width="20%">اسم العضو</th>
                            <th width="20%">المسمى الوظيفي</th>
                            <th width="20%">الصفة</th>
                            <th width="20%">البريد الإلكتروني</th>
                            <th width="20%">رقم الهاتف</th>
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

            self.email_sent = 1


