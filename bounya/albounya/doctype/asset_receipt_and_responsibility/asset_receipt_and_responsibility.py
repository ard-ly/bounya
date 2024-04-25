# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class AssetReceiptandResponsibility(Document):
    def on_submit(self):
        """set the custodian field of asset to entered on here"""

        for asset in self.asset_receipt_and_responsibility_table:
            asset = frappe.get_doc("Asset", asset)
            if asset.custodian:
                frappe.msgprint(_(f"Asset {asset.asset_name} Already got one!"))
                continue
            asset.custodian = self.custodian
            asset.save()

        frappe.db.commit()

