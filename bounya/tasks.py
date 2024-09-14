
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
import json
from frappe.utils import (
    flt,
    getdate,
    nowdate,
)


@frappe.whitelist()
def calculate_exp_yrears_in_employee():
    frappe.db.sql(
         f"""
         UPDATE tabEmployee AS e
         SET
         e.custom_total_insed_experience_in_years =DATEDIFF(NOW(), e.date_of_joining)/365 
             WHERE e.status = "Active";
         """)
    frappe.db.sql(
            f"""
            UPDATE tabEmployee AS e
            SET
            e.custom_total_experience_in_years  = (DATEDIFF(NOW(), e.date_of_joining)/365 + e.custom_total_external_experians_year )
                WHERE e.status = "Active";
            """)
    frappe.db.commit()
