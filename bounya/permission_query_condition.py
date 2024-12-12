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
    elif doctype == "Committee Extend":
        return get_committees_extend_perm(user, doctype)
    elif doctype == "Inbox":
        return get_inbox_perm(user, doctype)
    


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



    # Get Department Manager users
    departments_managers = frappe.db.sql_list("select user_id from `tabEmployee` where status='Active' and name in (select custom_department_manager from `tabDepartment` where custom_department_manager !='')")
    if frappe.session.user in departments_managers:
        user_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
        if user_emp:
            department_docs = frappe.get_all('Department', filters={"custom_department_manager": user_emp}, fields=["name"])
            for department_doc in department_docs:
                if department_doc:
                    mail_department_docs = frappe.get_all(doctype, filters={"from": department_doc.name})
                    for mail_department_doc in mail_department_docs:
                        allowed_docs_list.append(mail_department_doc.name)

                    mail_department_docs = frappe.get_all(doctype, filters={"to": department_doc.name})
                    for mail_department_doc in mail_department_docs:
                        allowed_docs_list.append(mail_department_doc.name)

                    copy_to_docs = frappe.get_all("Copy to Department",
                                             filters={"parenttype": doctype, "department": department_doc.name},
                                             fields=["parent"])
                    for copy_to_doc in copy_to_docs:
                        allowed_docs_list.append(copy_to_doc.parent)

                    marginalize_docs = frappe.get_all("Marginalize Department",
                                             filters={"parenttype": doctype, "department": department_doc.name},
                                             fields=["parent"])
                    for marginalize_doc in marginalize_docs:
                        allowed_docs_list.append(marginalize_doc.parent)


    if frappe.session.user == "Administrator":
        return

    if "Show All Mail" in frappe.get_roles(frappe.session.user):
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


    # Get Department Manager users
    departments_managers = frappe.db.sql_list("select user_id from `tabEmployee` where status='Active' and name in (select custom_department_manager from `tabDepartment` where custom_department_manager !='')")
    if frappe.session.user in departments_managers:
        user_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
        if user_emp:
            department_docs = frappe.get_all('Department', filters={"custom_department_manager": user_emp}, fields=["name"])
            for department_doc in department_docs:
                if department_doc:
                    mail_department_docs = frappe.get_all(doctype, filters={"issuing_authority": department_doc.name})
                    for mail_department_doc in mail_department_docs:
                        allowed_docs_list.append(mail_department_doc.name)


    # General Decision
    general_decision_docs = frappe.get_all(doctype, filters={"general_decision":1}, fields=["name"])
    for general_decision_doc in general_decision_docs:
        allowed_docs_list.append(general_decision_doc.name)


    # Specific Decision
    user_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
    if user_emp:
        specific_decision_docs = frappe.get_all(doctype, filters={"general_decision": 0}, fields=["name"])
        for specific_decision_doc in specific_decision_docs:
            specific_employees = frappe.db.sql_list("select user_id from `tabEmployee` where name in (select employee from `tabCopy to Employee` where parenttype='{0}' and parent='{1}')".format(doctype, specific_decision_doc.name))
            if frappe.session.user in specific_employees:
                allowed_docs_list.append(specific_decision_doc.name)


    # Get Department Manager users
    departments_managers = frappe.db.sql_list("select user_id from `tabEmployee` where status='Active' and name in (select custom_department_manager from `tabDepartment` where custom_department_manager !='')")
    if frappe.session.user in departments_managers:
        user_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
        if user_emp:
            department_docs = frappe.get_all('Department', filters={"custom_department_manager": user_emp}, fields=["name"])
            for department_doc in department_docs:
                if department_doc:
                    copy_to_docs = frappe.get_all("Copy to Department",
                                             filters={"parenttype": doctype, "department": department_doc.name},
                                             fields=["parent"])
                    for copy_to_doc in copy_to_docs:
                        allowed_docs_list.append(copy_to_doc.parent)


    if frappe.session.user == "Administrator":
        return

    if "Show All Decisions" in frappe.get_roles(frappe.session.user):
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))




def get_committees_perm(user, doctype):
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



    committee_members = frappe.get_all("Committee Members",
                                    filters={"parenttype":doctype,
                                             "email":frappe.session.user},
                                    fields=["parent"])
    for member in committee_members:
        allowed_docs_list.append(member.parent)


    if frappe.session.user == "Administrator":
        return

    if "Show All Committees" in frappe.get_roles(frappe.session.user):
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))





def get_committees_extend_perm(user, doctype):
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


    allowed_committees_extend = ''
    allowed_committees = get_committees_perm(user, "Committees")
    if allowed_committees:
        allowed_committees_extend = allowed_committees.replace('name', 'committee')


    if frappe.session.user == "Administrator":
        return

    if "Show All Committees" in frappe.get_roles(frappe.session.user):
        return
        
    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}') or {allowed_committees_extend}".format(allowed_list="','".join(allowed_docs_tuple), allowed_committees_extend= allowed_committees_extend)




def get_inbox_perm(user, doctype):
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


    # Get Department Manager users
    user_department_manager = []
    user_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
    if user_emp:
        users_department = frappe.db.sql_list("select name from `tabDepartment` where custom_department_manager='{0}'".format(user_emp))
        

    if frappe.session.user == "Administrator":
        return

    if "Show All Mail" in frappe.get_roles(frappe.session.user):
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}') or referral_to in ('{users_department}') ".format(allowed_list="','".join(allowed_docs_tuple), users_department= "','".join(users_department))




