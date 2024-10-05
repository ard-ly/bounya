
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

@frappe.whitelist()
def calculate_tower_age():
    
    towers_sql = frappe.db.sql(f""" select name,date_of_construction  from `tabTowers` """)
    for pare in towers_sql:
            if pare[1]:
                tower_doc=frappe.get_doc("Towers", pare[0])
                months_d=frappe.utils.month_diff(frappe.utils.nowdate(),tower_doc.date_of_construction)
                print(months_d)
                frappe.db.set_value('Towers', pare[0], 'age_of_tower', int(months_d))