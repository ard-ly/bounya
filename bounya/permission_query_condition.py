# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
import frappe
from frappe import _
from frappe.utils import getdate, cstr


def get_permission_query_conditions(user, doctype):
    if doctype in ["Incoming Mail", "Outgoing Mail"]:
        return get_mail_perm(user, doctype)
    elif doctype == "Decisions":
        return get_decisions_perm(user, doctype)
    elif doctype == "Committees":
        return get_committees_perm(user, doctype)
    


def get_mail_perm(user, doctype):
    allowed_docs_list = []
    owned_docs = frappe.get_all(doctype, filters={"owner":frappe.session.user})
    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])
    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)


    user_designation = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "designation") or None
    if user_designation:
        mail_designation_docs = frappe.get_all(doctype, filters={"from": user_designation})
        for mail_designation_doc in mail_designation_docs:
            allowed_docs_list.append(mail_designation_doc.name)

        mail_designation_docs = frappe.get_all(doctype, filters={"to": user_designation})
        for mail_designation_doc in mail_designation_docs:
            allowed_docs_list.append(mail_designation_doc.name)


    user_department = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "department") or None
    if user_department:
        mail_department_docs = frappe.get_all(doctype, filters={"from": user_department})
        for mail_department_doc in mail_department_docs:
            allowed_docs_list.append(mail_department_doc.name)

        mail_department_docs = frappe.get_all(doctype, filters={"to": user_department})
        for mail_department_doc in mail_department_docs:
            allowed_docs_list.append(mail_department_doc.name)


        copy_to_docs = frappe.get_all("Copy to Department",
                                 filters={"parenttype": doctype, "department": user_department},
                                 fields=["parent"])
        for copy_to_doc in copy_to_docs:
            allowed_docs_list.append(copy_to_doc.parent)


        marginalize_docs = frappe.get_all("Marginalize Department",
                                 filters={"parenttype": doctype, "department": user_department},
                                 fields=["parent"])
        for marginalize_doc in marginalize_docs:
            allowed_docs_list.append(marginalize_doc.parent)

    
    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))




def get_decisions_perm(user, doctype):
    allowed_docs_list = []
    owned_docs = frappe.get_all(doctype, filters={"owner":frappe.session.user})
    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)


    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])
    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)



    emp = frappe.get_value("Employee", filters={"user_id": frappe.session.user}, fieldname="name")
    allowed_docs = frappe.get_all("Decisions",
                                    filters={"employee_specific": 1, "employee": emp},
                                    fields=["name"])
    for allowed_doc in allowed_docs:
        allowed_docs_list.append(allowed_doc.name)


    # if frappe.session.user == "Administrator":
    #     return
    frappe.msgprint(str(allowed_docs_list))
    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))




def get_employee_perm(user, doctype):
    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    allowed_docs_list = []

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



def get_committees_perm(user, doctype):
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


   


