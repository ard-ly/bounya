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

@frappe.whitelist()
def filter_realty(doctype, txt, searchfield, start, page_len, filters):
    realty = frappe.db.sql(f""" select name,realty_type,branch from `tabRealty` where covered_space > 0 and available_area > 0 and docstatus = 1 """)
    return realty




@frappe.whitelist()
def fetch_employee_with_role(doctype, txt, searchfield, start, page_len, filters):
    users = frappe.db.sql(
			f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'مدير إدارة' or  role ='المدير العام') AND parenttype = 'User' AND parent != 'Administrator' """)
    users = frappe.db.sql(
        """ SELECT e.name, e.employee_name FROM `tabEmployee` e left join `tabHas Role` r on e.user_id = r.parent  
                                            WHERE e.user_id != ' ' and (r.role = 'مدير إدارة' or  r.role ='المدير العام')  and e.name like %(txt)s 
                                            limit %(page_len)s offset %(start)s""".format(),
        {"start": start, "page_len": page_len, "txt": "%%%s%%" % txt},
    )
    return users