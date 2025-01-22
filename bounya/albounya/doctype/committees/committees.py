# Copyright (c) 2024, Omar Jaber and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate
from bounya.permission_query_condition import send_workflow_notification


class Committees(Document):
    def validate(self):
        send_workflow_notification(self.doctype, self.name, self.workflow_state)

        
    def on_submit(self):
        self.change_committee_status()
        self.send_reward_notification()


    @frappe.whitelist()
    def get_employee_data(self, employee_name):
        emp = frappe.get_list("Employee", filters= {"name": employee_name}, fields = ["*"])[0]
        return emp


    @frappe.whitelist()
    def change_committee_status(self):
        current_date = getdate(nowdate())
        start_date = getdate(self.committee_from)
        end_date = getdate(self.committee_to)

        if current_date > end_date:
            frappe.db.set_value(self.doctype, self.get('name'), "committee_status", 'Outdated')
        elif start_date <= current_date <= end_date:
            frappe.db.set_value(self.doctype, self.get('name'), "committee_status", 'Active')
        else:
            frappe.db.set_value(self.doctype, self.get('name'), "committee_status", 'New')




    @frappe.whitelist()
    def send_reward_notification(self):
        reward_exists = any(item.reward for item in self.get('committee_members'))

        if reward_exists:
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

            recipients = []

            for member in self.committee_members:
                if member.email not in recipients:
                    recipients.append(member.email)


            decision = frappe.get_doc("Decisions", self.decision)
            for copy_to_department in decision.copy_to:
                department_manager = frappe.get_value("Department", filters = {"name": copy_to_department.department}, fieldname = "custom_department_manager") or None
                if department_manager:
                    employee_email = frappe.get_value("Employee", filters = {"name": department_manager}, fieldname = "user_id") or None
                    if employee_email:
                        if employee_email not in recipients:
                            recipients.append(employee_email)


            if len(recipients)>0:
                for recipient in self.committee_members:
                    if recipient.from_system:
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = recipient.email
                        new_doc.type = "Share"
                        new_doc.document_type = self.doctype
                        new_doc.document_name = self.name
                        new_doc.subject = f"تشكيل لجنة جديدة: {self.name}"
                        new_doc.insert(ignore_permissions=True)

                subject = f"تشكيل لجنة جديدة: {self.name}"
                frappe.sendmail(
                    recipients=recipients,
                    subject=subject,
                    message=message,
                    reference_doctype=self.doctype,
                    reference_name=self.name,
                    delayed=False
                )



