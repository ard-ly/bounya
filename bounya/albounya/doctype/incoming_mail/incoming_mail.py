# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class IncomingMail(Document):
    def on_submit(self):
        message = _("Referred to {0}").format(self.referral_to)
        self.status = message
        self.db_set("status", self.status)

    def autoname(self):
        year = self.message_registration_date[:4]
        short_year = year[-2:]
        
        count = frappe.db.count(
            'Incoming Mail',
            filters={
                'name': ['like', f"{short_year}-%"]
            }
        )
        
        sequence_number = count + 1
        
        formatted_sequence = f"{sequence_number:04d}"
        
        self.name = f"{short_year}-{formatted_sequence}"

        