# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Inbox(Document):
    def on_submit(self):
        self.update_mail_status()


    def update_mail_status(self):
        doc = frappe.get_doc(self.mail_type, self.mail_number)
        if doc:
            doc.status = self.result
            doc.save(ignore_permissions=True)
            frappe.msgprint(_('Mail status updated successfully'), alert=True, indicator='green')
