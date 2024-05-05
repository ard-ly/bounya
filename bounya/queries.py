from __future__ import unicode_literals
import frappe
from erpnext.controllers.queries import get_fields
from frappe.desk.reportview import get_filters_cond, get_match_cond


@frappe.whitelist()
def filter_sq_based_on_rfq(doctype, txt, searchfield, start, page_len, filters):
    active = filters.get("is_active", False)
    query = f"""
                SELECT ss.name 
                FROM `tabSalary Strucure` ss
                WHERE (is_active = '{active}'
            """
    return frappe.db.sql(query)
