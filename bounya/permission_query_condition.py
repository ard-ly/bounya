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
    
    # user_designation = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "designation") or None
    # if user_designation:
    #     mail_designation_docs = frappe.get_all(doctype, filters={"from": user_designation})
    #     for mail_designation_doc in mail_designation_docs:
    #         allowed_docs_list.append(mail_designation_doc.name)

    #     mail_designation_docs = frappe.get_all(doctype, filters={"to": user_designation})
    #     for mail_designation_doc in mail_designation_docs:
    #         allowed_docs_list.append(mail_designation_doc.name)


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

                    # marginalize_docs = frappe.get_all("Marginalize Department",
                    #                          filters={"parenttype": doctype, "department": department_doc.name},
                    #                          fields=["parent"])
                    # for marginalize_doc in marginalize_docs:
                    #     allowed_docs_list.append(marginalize_doc.parent)



    if "General Manager" in frappe.get_roles(frappe.session.user):
        # Get all employees who are assigned the "Chairman Manager" role
        chairman_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", frappe.get_all("Has Role", filters={"role": "Chairman Manager"}, pluck="parent")]},
            fields=["name"]
        )
        chairman_employee_names = [ce["name"] for ce in chairman_employees]

        # Get all departments
        all_departments = frappe.get_all("Department", fields=["name", "custom_department_manager"])

        # Filter departments to exclude those managed by a Chairman Manager
        excluded_departments = [
            dept["name"]
            for dept in all_departments
            if dept.get("custom_department_manager") in chairman_employee_names
        ]

        # Collect all documents for the specified doctype
        all_documents = frappe.get_all(doctype, fields=["name", "from", "to"])

        # Initialize the allowed docs list
        allowed_docs_list = []

        for doc in all_documents:
            if doc.get("from") not in excluded_departments and doc.get("to") not in excluded_departments:
                allowed_docs_list.append(doc["name"])

        # Include documents from the "Copy to Department" table
        copy_to_docs = frappe.get_all(
            "Copy to Department",
            filters={"parenttype": doctype, "department": ["not in", excluded_departments]},
            fields=["parent"]
        )
        allowed_docs_list.extend([doc["parent"] for doc in copy_to_docs])

        # Remove duplicates (if any)
        allowed_docs_list = list(set(allowed_docs_list))




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



    if frappe.session.user == "Administrator":
        return

    if "Show All Mail" in frappe.get_roles(frappe.session.user):
        return

    if "Chairman Manager" in frappe.get_roles(frappe.session.user):
        return


    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))




def get_decisions_perm(user, doctype):
    allowed_docs_list = []

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




    if "General Manager" in frappe.get_roles(frappe.session.user):
        # Get all employees who are assigned the "Chairman Manager" role
        chairman_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", frappe.get_all("Has Role", filters={"role": "Chairman Manager"}, pluck="parent")]},
            fields=["name"]
        )
        chairman_employee_names = [ce["name"] for ce in chairman_employees]

        # Get all departments
        all_departments = frappe.get_all("Department", fields=["name", "custom_department_manager"])

        # Filter departments to exclude those managed by a Chairman Manager
        excluded_departments = [
            dept["name"]
            for dept in all_departments
            if dept.get("custom_department_manager") in chairman_employee_names
        ]

        # Filter documents based on excluded departments and `issuing_authority`
        department_docs = frappe.get_all(
            doctype,
            filters={"issuing_authority": ["not in", excluded_departments]},
            fields=["name"]
        )
        for doc in department_docs:
            allowed_docs_list.append(doc["name"])



    if "Office Manager" in frappe.get_roles(frappe.session.user):
        if frappe.session.user in get_chairman_and_general_office_managers_users():
            return



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



    if frappe.session.user == "Administrator":
        return

    if "Show All Decisions" in frappe.get_roles(frappe.session.user):
        return

    if "Chairman Manager" in frappe.get_roles(frappe.session.user):
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))




def get_committees_perm(user, doctype):
    allowed_docs_list = []
    

    committee_members = frappe.get_all("Committee Members",
                                    filters={"parenttype":doctype,
                                             "email":frappe.session.user},
                                    fields=["parent"])
    for member in committee_members:
        allowed_docs_list.append(member.parent)


    allowed_decisions = ''
    user_decisions = get_decisions_perm(user, "Decisions")
    if user_decisions:
        allowed_decisions = user_decisions.replace('name', 'decision')


    if "Office Manager" in frappe.get_roles(frappe.session.user):
        if frappe.session.user in get_chairman_and_general_office_managers_users():
            return


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


    if frappe.session.user == "Administrator":
        return

    if "Show All Committees" in frappe.get_roles(frappe.session.user):
        return

    if "Chairman Manager" in frappe.get_roles(frappe.session.user):
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}') or {allowed_decisions}".format(allowed_list="','".join(allowed_docs_tuple), allowed_decisions= allowed_decisions)





def get_committees_extend_perm(user, doctype):
    allowed_docs_list = []
    

    allowed_committees_extend = ''
    allowed_committees = get_committees_perm(user, "Committees")
    if allowed_committees:
        allowed_committees_extend = allowed_committees.replace('name', 'committee')


    if "Office Manager" in frappe.get_roles(frappe.session.user):
        if frappe.session.user in get_chairman_and_general_office_managers_users():
            return


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


    if frappe.session.user == "Administrator":
        return

    if "Show All Committees" in frappe.get_roles(frappe.session.user):
        return

    if "Chairman Manager" in frappe.get_roles(frappe.session.user):
        return
        
    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}') or {allowed_committees_extend}".format(allowed_list="','".join(allowed_docs_tuple), allowed_committees_extend= allowed_committees_extend)




def get_inbox_perm(user, doctype):
    allowed_docs_list = []

    # Get Department Manager users
    user_department_manager = []
    user_emp = frappe.get_value("Employee", filters = {"user_id": frappe.session.user}, fieldname = "name") or None
    if user_emp:
        users_department = frappe.db.sql_list("select name from `tabDepartment` where custom_department_manager='{0}'".format(user_emp))
        

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

        
    if frappe.session.user == "Administrator":
        return

    if "Show All Mail" in frappe.get_roles(frappe.session.user):
        return

    if "Chairman Manager" in frappe.get_roles(frappe.session.user):
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}') or referral_to in ('{users_department}') ".format(allowed_list="','".join(allowed_docs_tuple), users_department= "','".join(users_department))




def get_chairman_and_general_office_managers_users():
    office_manager_users = []

    chairman_general_managers_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", frappe.get_all("Has Role", filters={"role": ["in", ['Chairman Manager', 'General Manager']]}, pluck="parent")]},
            fields=["name", "user_id"]
        )

    for chairman_general_manager_employee in chairman_general_managers_employees:
        chairman_general_managers_departments = frappe.get_all(
            "Department",
            filters={"custom_department_manager": chairman_general_manager_employee.name, "disabled": 0},
            fields=["name", "custom_office_manager"]
        )
        for chairman_general_managers_department in chairman_general_managers_departments:
            if chairman_general_managers_department.custom_office_manager:
                office_manager_user = frappe.get_value("Employee", filters = {"name": chairman_general_managers_department.custom_office_manager}, fieldname = "user_id") or None
                if office_manager_user and office_manager_user not in office_manager_users:
                    office_manager_users.append(office_manager_user)
    
    return office_manager_users



def send_workflow_notification(doctype, document, workflow_state):
    allowed_users = []
    notification_subject = ''
    email_subject = ''
    msg = ''

    if workflow_state == 'Create By Legal Management':
        allowed_users = get_chairman_and_general_office_managers_users()
        if doctype=='Decisions':
            notification_subject = "يوجد قرار جديد بحاجة للمراجعة."
            email_subject = "مراجعة قرار"
        elif doctype=='Committees':
            notification_subject = "يوجد لجنة جديدة بحاجة للمراجعة."
            email_subject = "مراجعة لجنة"
        elif doctype=='Committee Extend':
            notification_subject = "يوجد طلب تمديد لجنة جديد بحاجة للمراجعة."
            email_subject = "مراجعة تمديد لجنة"

    elif workflow_state == 'Approved By Office Manager':
        allowed_users = frappe.db.sql_list("select parent from `tabHas Role` where role in ('General Manager', 'Chairman Manager') and parenttype='User' and parent !='Administrator' group by parent")
        if doctype=='Decisions':
            notification_subject = "يوجد قرار بحاجة للاعتماد."
            email_subject = "اعتماد قرار"
        elif doctype=='Committees':
            notification_subject = "يوجد لجنة جديدة بحاجة للاعتماد."
            email_subject = "اعتماد لجنة"
        elif doctype=='Committee Extend':
            notification_subject = "يوجد طلب تمديد لجنة جديد بحاجة للاعتماد."
            email_subject = "اعتماد تمديد لجنة"


    inbox_url = frappe.utils.data.get_url_to_form(doctype, document)
    if doctype=='Decisions':
        msg = "<p> You have a new Decision,<br> please check the decision and submit<br> <b><a href='{0}'>Go to Decision</a></b>".format(inbox_url)
    elif doctype=='Committees':
        mesg = "<p> You have a new Committee,<br> please check the committee and submit<br> <b><a href='{0}'>Go to Committee</a></b>".format(inbox_url)
    elif doctype=='Committee Extend':
        mesg = "<p> You have a new Committee Extend,<br> please check the committee extend and submit<br> <b><a href='{0}'>Go to Committee Extend</a></b>".format(inbox_url)


    for allowed_user in allowed_users:
        if allowed_user:
            try:
                new_doc = frappe.new_doc("Notification Log")
                new_doc.from_user = frappe.session.user
                new_doc.for_user = allowed_user
                new_doc.type = "Share"
                new_doc.document_type = doctype
                new_doc.document_name = document
                new_doc.subject = notification_subject
                new_doc.insert(ignore_permissions=True)

                frappe.sendmail(
                  recipients=allowed_user,
                  subject=email_subject,
                  message= msg,
                  now=1,
                  retry=3
                )
            except Exception as e:
                # Log errors for each user separately
                frappe.log_error(
                    message=f"Error sending workflow notification to user {allowed_user}: {str(e)}",
                    title="Workflow Notification Error"
                )






