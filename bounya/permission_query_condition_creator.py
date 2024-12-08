# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
import frappe
from frappe import _
from frappe.utils import getdate, cstr


def get_permission_query_conditions(user, doctype):
    if doctype == "Incoming Mail":
        return get_incoming_mail_perm(user)
    elif doctype == "Committees":
        return get_committees_perm(user)
    elif doctype == "Decisions":
        return get_decisions_perm(user)


def get_incoming_mail_perm(user, doctype):
    allowed_docs = frappe.get_all("Custom User Permission",
                                    filters={"applicable_for":doctype,
                                             "user":frappe.session.user},
                                    fields=["document"])

    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    allowed_docs_list = []
    for allowed_doc in allowed_docs:
        allowed_docs_list.append(allowed_doc.document)

    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)

    if frappe.session.user == "Administrator":
        return

    emps = frappe.get_all("Employee",filters={"user_id":frappe.session.user})
    if emps:
        apps = frappe.get_all(doctype,filters={"employee":emps[0].name})
        if apps:
            for app in apps:
                if app.name not in allowed_docs_list:
                    allowed_docs_list.append(app.name)

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))


                
def get_employee_perm(user):
    doctype = "Employee"
    allowed_docs = frappe.get_all("Custom User Permission",
                                    filters={"applicable_for":doctype,
                                             "user":frappe.session.user},
                                    fields=["document"])

    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    allowed_docs_list = []
    for allowed_doc in allowed_docs:
        allowed_docs_list.append(allowed_doc.document)

    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)

    # Get Department users
    if frappe.session.user in frappe.db.sql_list("select user_id from `tabEmployee` where status='Active' and name in (select custom_department_manager from `tabDepartment` where custom_department_manager !='')"):
        employee_department = frappe.get_value("Employee", filters={"user_id": frappe.session.user}, fieldname="department")

        emps = frappe.get_all("Employee",filters={"department": employee_department})
        if emps:
            for emp in emps:
                apps = frappe.get_all(doctype,filters={"name":emp.name})
                if apps:
                    for app in apps:
                        if app.name not in allowed_docs_list:
                            allowed_docs_list.append(app.name)

        allowed_docs_tuple = tuple(allowed_docs_list)


    # Get direct manager users
    session_emp = frappe.get_value("Employee", filters={"user_id": frappe.session.user}, fieldname="name")
    emps = frappe.get_all("Employee",filters={"reports_to": session_emp})
    if emps:
        for emp in emps:
            apps = frappe.get_all(doctype,filters={"name":emp.name})
            if apps:
                for app in apps:
                    if app.name not in allowed_docs_list:
                        allowed_docs_list.append(app.name)

    allowed_docs_tuple = tuple(allowed_docs_list)
        


    emps = frappe.get_all("Employee",filters={"user_id":frappe.session.user})
    if emps:
        apps = frappe.get_all(doctype,filters={"name":emps[0].name})
        if apps:
            for app in apps:
                if app.name not in allowed_docs_list:
                    allowed_docs_list.append(app.name)

    allowed_docs_tuple = tuple(allowed_docs_list)

    if frappe.session.user == "Administrator":
        return

    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))



def get_committees_perm(user):
    doctype = "Committees"
    allowed_docs = frappe.get_all("Custom User Permission",
                                    filters={"applicable_for":doctype,
                                             "user":frappe.session.user},
                                    fields=["document"])

    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    committee_members = frappe.get_all("Committee Prosecutor",
                                    filters={"parenttype":doctype,
                                             "email":frappe.session.user},
                                    fields=["parent"])

    allowed_docs_list = []
    for allowed_doc in allowed_docs:
        allowed_docs_list.append(allowed_doc.document)

    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)

    for member in committee_members:
        allowed_docs_list.append(member.parent)


    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))


   
def get_decisions_perm(user):
    doctype = "Decisions"
    emp = frappe.get_value("Employee", filters={"user_id": frappe.session.user}, fieldname="name")

    allowed_docs = frappe.get_all("Decisions",
                                    filters={"employee_specific": 1, "employee": emp},
                                    fields=["name"])

    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    allowed_docs_list = []
    for allowed_doc in allowed_docs:
        allowed_docs_list.append(allowed_doc.name)

    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)

    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))


