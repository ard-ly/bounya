# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import datetime

class OutgoingMail(Document):
    def after_insert(self):
        department_manager = frappe.get_value("Department", filters = {"name": self.referral_to}, fieldname = "custom_department_manager") or None
        if department_manager:
            department_managerـuser = frappe.get_value("Employee", filters = {"name": department_manager}, fieldname = "user_id") or None
            if department_managerـuser:
                new_doc = frappe.new_doc("Notification Log")
                new_doc.from_user = frappe.session.user
                new_doc.for_user = department_managerـuser
                new_doc.type = "Share"
                new_doc.document_type = self.doctype
                new_doc.document_name = self.name
                new_doc.subject = "يوجد بريد وارد جديد بحاجة للاعتماد."
                new_doc.insert(ignore_permissions=True)

                inbox_url = frappe.utils.data.get_url_to_form(self.doctype, self.name)
                mesg = "<p> You have a new Outgoing mail,<br> please check the mail and submit<br> <b><a href='{0}'>Go to Mail</a></b>".format(inbox_url)
                frappe.sendmail(
                  recipients=department_managerـuser,
                  subject="بريد صادر جديد",
                  message= mesg,
                  now=1,
                  retry=3
                )


    def on_submit(self):
        message = _("Referred to {0}").format(self.referral_to)
        self.status = message
        self.db_set("status", self.status)

        self.create_inbox()

    def autoname(self):
        # Ensure `message_registration_date` is in string format
        if isinstance(self.message_registration_date, datetime.date):
            year = self.message_registration_date.strftime("%Y")  # Convert to string and extract year
        else:
            year = str(self.message_registration_date)[:4]

        short_year = year[-2:]
        count = frappe.db.count(
            'Outgoing Mail',
            filters={
                'name': ['like', f"{short_year}-%"]
            }
        )
        sequence_number = count + 1
        formatted_sequence = f"{sequence_number:04d}"
        self.name = f"{short_year}-{formatted_sequence}"


    def create_inbox(self):
        doc = frappe.new_doc("Inbox")
        doc.mail_type = self.doctype
        doc.mail_number = self.name
        doc.referral_to = self.referral_to
        doc.message_subject = self.message_subject
        doc.flags.ignore_mandatory = True
        doc.save(ignore_permissions=True)

        department_manager = frappe.get_value("Department", filters = {"name": self.referral_to}, fieldname = "custom_department_manager") or None
        if department_manager:
            department_managerـuser = frappe.get_value("Employee", filters = {"name": department_manager}, fieldname = "user_id") or None
            if department_managerـuser:
                new_doc = frappe.new_doc("Notification Log")
                new_doc.from_user = frappe.session.user
                new_doc.for_user = department_managerـuser
                new_doc.type = "Share"
                new_doc.document_type = "Inbox"
                new_doc.document_name = doc.name
                new_doc.subject = "You have a new referred mail."
                new_doc.insert(ignore_permissions=True)

                inbox_url = frappe.utils.data.get_url_to_form("Inbox", doc.name)
                mesg = "<p> You have a new referred mail,<br> please check the inbox and add the result<br> <b><a href='{0}'>Go to Inbox</a></b>".format(inbox_url)
                frappe.sendmail(
                  recipients=department_managerـuser,
                  subject="You have a new referred mail.",
                  message= mesg,
                  now=1,
                  retry=3
                )
                frappe.db.commit()


    @frappe.whitelist()
    def get_session_office_manager_user_entity(self):
        office_manager_department = None

        session_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
        if session_emp:
            office_manager_department = frappe.get_value("Department", filters = {"custom_office_manager": session_emp}, fieldname = "name") or None

        return office_manager_department

