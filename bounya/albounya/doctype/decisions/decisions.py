# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from bounya.permission_query_condition import send_workflow_notification

class Decisions(Document):
    def validate(self):
        send_workflow_notification(self.doctype, self.name, self.workflow_state)


    def on_submit(self):
        self.send_decisions_notification()


    @frappe.whitelist()
    def send_decisions_notification(self):
        if self.general_decision:
            employee_emails = frappe.db.sql_list("select user_id from `tabEmployee` where status='Active'")
            for employee_email in employee_emails:
                new_doc = frappe.new_doc("Notification Log")
                new_doc.from_user = frappe.session.user
                new_doc.for_user = employee_email
                new_doc.type = "Share"
                new_doc.document_type = self.doctype
                new_doc.document_name = self.name
                new_doc.subject = _("New General Decision")
                new_doc.insert(ignore_permissions=True)

                decision_url = frappe.utils.data.get_url_to_form(self.doctype, self.name)
                message = f"""
                    <div style='direction: rtl; text-align: right;'>
                        تم إصدار قرار عام جديد <b><a href='{decision_url}'>{self.decision_subject}</a></b>
                    </div>
                """
                frappe.sendmail(
                  recipients=employee_email,
                  subject="قرار عام جديد",
                  message= message,
                  now=1,
                  retry=3
                )
                frappe.db.commit()
        else:
            for employee_name in self.copy_to_employee:
                if employee_name:
                    employee_email = frappe.get_value("Employee", filters = {"name": employee_name.employee}, fieldname = "user_id") or None
                    if employee_email:
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = employee_email
                        new_doc.type = "Share"
                        new_doc.document_type = self.doctype
                        new_doc.document_name = self.name
                        new_doc.subject = _("New Decision")
                        new_doc.insert(ignore_permissions=True)

                        decision_url = frappe.utils.data.get_url_to_form(self.doctype, self.name)
                        message = f"""
                            <div style='direction: rtl; text-align: right;'>
                                تم إصدار قرار جديد <b><a href='{decision_url}'>{self.decision_subject}</a></b>
                            </div>
                        """
                        frappe.sendmail(
                          recipients=employee_email,
                          subject="قرار جديد",
                          message= message,
                          now=1,
                          retry=3
                        )
                        frappe.db.commit()

            for copy_to_department in self.copy_to:
                department_manager = frappe.get_value("Department", filters = {"name": copy_to_department.department}, fieldname = "custom_department_manager") or None
                if department_manager:
                    employee_email = frappe.get_value("Employee", filters = {"name": department_manager}, fieldname = "user_id") or None
                    if employee_email:
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = employee_email
                        new_doc.type = "Share"
                        new_doc.document_type = self.doctype
                        new_doc.document_name = self.name
                        new_doc.subject = _("New Decision")
                        new_doc.insert(ignore_permissions=True)

                        decision_url = frappe.utils.data.get_url_to_form(self.doctype, self.name)
                        message = f"""
                            <div style='direction: rtl; text-align: right;'>
                                تم إصدار قرار جديد <b><a href='{decision_url}'>{self.decision_subject}</a></b>
                            </div>
                        """
                        frappe.sendmail(
                          recipients=employee_email,
                          subject="قرار جديد",
                          message= message,
                          now=1,
                          retry=3
                        )
                        frappe.db.commit()


