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

@frappe.whitelist()
def filter_office(doctype, txt, searchfield, start, page_len, filters):
    branch = filters.get('branch')
    offices = frappe.db.sql(f""" select office_name from `tabBranches Offices` where parent = '{branch}' """)
    return offices

@frappe.whitelist()
def filter_customer_based_on_users(doctype, txt, searchfield, start, page_len, filters):
    user = filters.get('user')
    customer = frappe.db.sql(f""" select name from `tabCustomer` where custom_user = '{user}' """)
    return customer

# @frappe.whitelist()
# def filter_realty(doctype, txt, searchfield, start, page_len, filters):
#     realty = frappe.db.sql(f""" select name,realty_type,branch from `tabRealty` where covered_space > 0 and available_area > 0 and docstatus = 1 """)
#     return realty