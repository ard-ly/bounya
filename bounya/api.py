import re
import frappe
from datetime import date
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, today
from frappe.utils.data import money_in_words, getdate, nowdate, add_days, add_months, add_years
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

import erpnext
import re

# from scipy import interpolate
# from scipy.interpolate import CubicSpline

# Hadeel Commite this code

# @frappe.whitelist()
# def make_demo_data(
#     doc,
#     salary_structure,
#     marital_status,
#     number_of_children,
#     base,
#     evaluation,
#     performance_factor,
# ):
#     try:
#         employee = frappe.new_doc("Employee")
#         employee.first_name = "Demo"
#         employee.gender = "Male"
#         employee.date_of_birth = "1990-01-01"
#         employee.date_of_joining = "2020-01-01"
#         employee.holiday_list = "h1"
#         # employee.marital_status = 'Married'
#         employee.marital_status = marital_status
#         employee.custom_number_of_children = number_of_children
#         employee.insert()

#         # calculate family and housing
#         if employee.marital_status == "Single":
#             family_allowance = 0
#             housing_allowance = 100
#         elif (
#             employee.marital_status == "Married"
#             and employee.custom_number_of_children == 1
#         ):
#             family_allowance = 200
#             housing_allowance = 200
#         elif (
#             employee.marital_status == "Married"
#             and employee.custom_number_of_children != 1
#         ):
#             family_allowance = 100
#             housing_allowance = 150

#         # salary_structure = 'st1'
#         salary_structure_assignment = frappe.new_doc(
#             "Salary Structure Assignment")
#         salary_structure_assignment.employee = employee.name
#         salary_structure_assignment.salary_structure = salary_structure
#         salary_structure_assignment.from_date = "2023-01-01"
#         salary_structure_assignment.custom_evaluation = evaluation
#         salary_structure_assignment.custom_performance_factor = performance_factor
#         salary_structure_assignment.custom_family_allowance = family_allowance
#         salary_structure_assignment.custom_housing_allowance = housing_allowance
#         salary_structure_assignment.base = base
#         salary_structure_assignment.insert()
#         salary_structure_assignment.submit()

#         salary_slip = frappe.new_doc("Salary Slip")
#         salary_slip.employee = employee.name
#         salary_slip.posting_date = "2024-01-01"
#         # salary_slip.salary_structure = salary_structure
#         salary_slip.insert()
#         salary_slip.employee = ""
#         salary_slip.employee = employee.name
#         salary_slip.save()
#         net_pay = salary_slip.net_pay
#         # delete transection sample data
#         frappe.delete_doc("Salary Slip", salary_slip.name)
#         salary_structure_assignment.cancel()
#         frappe.delete_doc("Salary Structure Assignment",
#                           salary_structure_assignment.name)
#         frappe.delete_doc("Employee", employee.name)
#         # print("Salary Net gross : " , salary_slip.net_pay)
#         return base, net_pay
#     except Exception as e:
#         msg = _(e)
#         frappe.throw(msg, title=_("Error"))
#         frappe.msgprint(e)

# this code work in employee fileds for bank branches



def update_employee_status(doc, method):
    if doc.leave_type=='إجازة بدون مرتب':
        emp = frappe.get_doc("Employee", doc.employee)
        emp.status='Suspended'
        emp.custom_stop_resune='إجازة بدون مرتب'
        emp.flags.ignore_mandatory = True
        emp.save(ignore_permissions=True)


@frappe.whitelist()
def send_committeesـreward_reminder_notification():
    current_date = getdate(nowdate())

    all_committees = frappe.get_all(
        'Committees',
        filters={
            'docstatus': 1,
            'committee_from': ['<=', current_date],
            'committee_to': ['>=', current_date]
        },
        fields=['name']
    )
    committees_with_reward = []

    for committee in all_committees:
        doc = frappe.get_doc('Committees', committee.name)
        
        if any(item.reward for item in doc.get('committee_members')):
            committees_with_reward.append(committee)
    
    for committee in committees_with_reward:
        doc = frappe.get_doc('Committees', committee.name)

        blocked_users = ['Administrator']
        hr_managers = frappe.get_all('Has Role', filters={'role': 'HR Manager', 'parenttype': 'User'}, fields=['parent'])
        
        hr_manager_emails = [
            manager['parent'] 
            for manager in hr_managers 
            if manager['parent'] not in blocked_users
        ]

        committee_from_date = getdate(doc.committee_from)
        
        if hr_manager_emails and current_date.day == committee_from_date.day:

            link = frappe.utils.get_url_to_form(doc.doctype, doc.name)

            table_rows = ''
            for item in doc.get('committee_members'):
                table_rows += f"""
                <tr>
                    <td>{item.idx}</td>
                    <td>{item.member_name}</td>
                    <td>{item.designation}</td>
                    <td>{item.email}</td>
                    <td>{item.phone_number}</td>
                </tr>
                """

            message = f"""
            <div style='direction: rtl; text-align: right;'>
                تذكير بمكافآت اللجنة: <a href='{link}'>{doc.name}</a>, للأعضاء التاليين:<br><br>
                <table border="1" class="text-center" style="border-collapse: collapse; width: 70%;">
                    <thead>
                        <tr>
                            <th width="3%">م</th>
                            <th width="20%">اسم العضو</th>
                            <th width="20%">المسمى الوظيفي</th>
                            <th width="20%">البريد الإلكتروني</th>
                            <th width="20%">رقم الهاتف</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            """

            subject = f"تذكير: مكافآت لجنة : {doc.name}"
            frappe.sendmail(
                recipients=hr_manager_emails,
                subject=subject,
                message=message,
                reference_doctype=doc.doctype,
                reference_name=doc.name,
                delayed=False
            )
            print(doc.name)



@frappe.whitelist()
def check_outdated_committees():
    committees = frappe.get_all('Committees', filters={'committee_status': ['!=', 'Outdated']}, fields=['name', 'committee_from', 'committee_to', 'committee_status'])
    for committee in committees:
        current_date = getdate(nowdate())
        start_date = getdate(committee.committee_from)
        end_date = getdate(committee.committee_to)

        if current_date > end_date:
            frappe.db.sql("update `tabCommittees` set committee_status='Outdated' where name='{0}'".format(committee.name))
            frappe.db.commit()
        elif start_date <= current_date <= end_date:
            frappe.db.sql("update `tabCommittees` set committee_status='Active' where name='{0}'".format(committee.name))
            frappe.db.commit()
        else:
            frappe.db.sql("update `tabCommittees` set committee_status='New' where name='{0}'".format(committee.name))
            frappe.db.commit()



@frappe.whitelist()
def notification_end_contract_duration():
    employees = frappe.get_all(
        'Employee', 
        filters={
            'status': ['=', 'Active'], 
            'custom_contract_type': ['=', 'محدد المدة']
        }, 
        fields=['name', 'custom_contract_duration', 'date_of_joining']
    )

    for emp in employees:
        if emp.custom_contract_duration:
            notification_send_date = []
            
            if emp.custom_contract_duration=='سنة':
                contract_end_date = add_years(emp.date_of_joining, 1)
            elif emp.custom_contract_duration=='ستة أشهر':
                contract_end_date = add_months(emp.date_of_joining, 6)
            else:
                contract_end_date = emp.date_of_joining

            days_left = (getdate(contract_end_date) - getdate(nowdate())).days

            notification_send_date.append(add_months(contract_end_date, -1)) if add_months(contract_end_date, -1) > getdate(nowdate()) else None
            notification_send_date.append(add_days(contract_end_date, -7)) if add_days(contract_end_date, -7) > getdate(nowdate()) else None

            if getdate(nowdate()) in notification_send_date:
                hr_notification_users = frappe.get_all('Has Role', filters={'role': 'HR Notification', 'parent': ['!=', 'Administrator']}, fields=['parent'])
                if hr_notification_users and days_left>0:
                    for user in hr_notification_users:
                        print(f"""Employee {emp.name}, will end his contract after {days_left} days""")
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = user.parent
                        new_doc.type = "Share"
                        new_doc.document_type = "Employee"
                        new_doc.document_name = emp.name
                        new_doc.subject = f"""Employee {emp.name}, will end his contract after {days_left} days"""
                        new_doc.insert(ignore_permissions=True)

           

@frappe.whitelist()
def notification_reaching_retirement_age():
    employees = frappe.get_all(
        'Employee', 
        filters={
            'status': ['=', 'Active']
        }, 
        fields=['name', 'date_of_retirement']
    )

    for emp in employees:
        if emp.date_of_retirement:
            notification_send_date = []
            
            days_left = (getdate(emp.date_of_retirement) - getdate(nowdate())).days

            notification_send_date.append(add_months(emp.date_of_retirement, -1)) if add_months(emp.date_of_retirement, -1) > getdate(nowdate()) else None
            notification_send_date.append(add_days(emp.date_of_retirement, -7)) if add_days(emp.date_of_retirement, -7) > getdate(nowdate()) else None

            if getdate(nowdate()) in notification_send_date:
                hr_notification_users = frappe.get_all('Has Role', filters={'role': 'HR Notification', 'parent': ['!=', 'Administrator']}, fields=['parent'])
                if hr_notification_users and days_left>0:
                    for user in hr_notification_users:
                        print(f"""Employee {emp.name}, will reach age of retirement after {days_left} days""")
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = user.parent
                        new_doc.type = "Share"
                        new_doc.document_type = "Employee"
                        new_doc.document_name = emp.name
                        new_doc.subject = f"""Employee {emp.name}, will reach age of retirement after {days_left} days"""
                        new_doc.insert(ignore_permissions=True)     



@frappe.whitelist()
def notification_employee_promotion():
    employees = frappe.get_all(
        'Employee', 
        filters={
            'status': ['=', 'Active']
        }, 
        fields=['name', 'date_of_joining']
    )

    for emp in employees:
        if emp.date_of_joining:
            notification_send_date = []
            
            emp_joining_year = getdate(emp.date_of_joining).year
            
            if getdate(nowdate()).month > getdate(emp.date_of_joining).month or (getdate(nowdate()).month == getdate(emp.date_of_joining).month and getdate(nowdate()).day > getdate(emp.date_of_joining).day):
                emp_joining_year += 1            
            next_promotion_date = getdate(f"{emp_joining_year}-{getdate(emp.date_of_joining).month:02d}-{getdate(emp.date_of_joining).day:02d}")

            days_left = (getdate(next_promotion_date) - getdate(nowdate())).days

            notification_send_date.append(add_months(next_promotion_date, -1)) if add_months(next_promotion_date, -1) > getdate(nowdate()) else None
            notification_send_date.append(add_days(next_promotion_date, -7)) if add_days(next_promotion_date, -7) > getdate(nowdate()) else None

            if getdate(nowdate()) in notification_send_date:
                hr_notification_users = frappe.get_all('Has Role', filters={'role': 'HR Notification', 'parent': ['!=', 'Administrator']}, fields=['parent'])
                if hr_notification_users and days_left>0:
                    for user in hr_notification_users:
                        print(f"""Employee {emp.name}, next promotion after {days_left} days""")
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = user.parent
                        new_doc.type = "Share"
                        new_doc.document_type = "Employee"
                        new_doc.document_name = emp.name
                        new_doc.subject = f"""Employee {emp.name}, next promotion after {days_left} days"""
                        new_doc.insert(ignore_permissions=True)

           

@frappe.whitelist()
def notification_end_leave_application():
    leaves = frappe.get_all(
        'Leave Application', 
        filters={
            'docstatus': ['=', 1]
        }, 
        fields=['name', 'employee', 'to_date']
    )

    for leave in leaves:
        if leave.to_date:
            return_date = getdate(add_days(leave.to_date, 1))

            if getdate(nowdate()) == getdate(return_date):
                hr_notification_users = frappe.get_all('Has Role', filters={'role': 'HR Notification', 'parent': ['!=', 'Administrator']}, fields=['parent'])
                if hr_notification_users:
                    for user in hr_notification_users:
                        print(f"Employee {leave.employee} has completed their leave and is returning to work today.")
                        new_doc = frappe.new_doc("Notification Log")
                        new_doc.from_user = frappe.session.user
                        new_doc.for_user = user.parent
                        new_doc.type = "Share"
                        new_doc.document_type = "Leave Application"
                        new_doc.document_name = leave.name
                        new_doc.subject = f"Employee {leave.employee} has completed their leave and is returning to work today."
                        new_doc.insert(ignore_permissions=True)

           


@frappe.whitelist()
def get_salary_components(doc):
    components = []
    component_list = frappe.db.get_all(
        'Salary Component Settings', fields=['salary_component'],)

    for c in component_list:
        components.append(str(c.salary_component))
    return components

@frappe.whitelist()
def recalculate_salary_slip(doc):
    print("Calculating LLLLLLLLLLLLLLLL")
    salary_slip_list =frappe.db.get_all("Salary Slip"  , filters={'payroll_entry' :doc} , fields=['name'] , pluck='name')
    count = 0
    for slip in salary_slip_list:

        try:
            s= frappe.get_doc("Salary Slip" , slip)
            s.validate()
            s.save()
            frappe.db.commit()
            count = count + 1
            frappe.publish_progress(count * 100 / len(salary_slip_list), title=_("Updating Salary Slip..."))

        except:
            print ("can not save salary slip update")

    print("llllllllllllllllllllllllllll" , count)
    return count

@frappe.whitelist()
def fetch_bank_branch_list(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """
        SELECT branch_name
        FROM `tabEmployee Bank Branch`
        WHERE parent = %(bank_name)s
        and `branch_name` LIKE %(txt)s
        """.format(
            key=searchfield
        ),
        {
            "txt": "%%%s%%" % txt,
            "start": start,
            "page_len": page_len,
            "bank_name": filters.get("bank_name"),
        },
    )


# this code work in employee fileds for office branches
@frappe.whitelist()
def fetch_branchs_office_list(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """
        SELECT office_name
        FROM `tabBranches Offices`
        WHERE parent = %(branch)s
        and `office_name` LIKE %(txt)s
        """.format(
            key=searchfield
        ),
        {
            "txt": "%%%s%%" % txt,
            "start": start,
            "page_len": page_len,
            "branch": filters.get("branch"),
        },
    )


@frappe.whitelist()
def fetch_base_from_slip(grade, marbot):
    grade = frappe.get_doc("Employee Grade", grade)
    if cint(marbot) > 0:
        return grade.default_base_pay + (
            grade.custom_dependent_value * (cint(marbot) - 1)
        )
    else:
        return grade.default_base_pay


@frappe.whitelist()
def update_base_from_slip(doc, method):
    # frappe.msgprint("hi")
    if doc.grade:
        grade = frappe.get_doc("Employee Grade", doc.grade)
        if cint(doc.custom_dependent) > 0:
            doc.custom_net_salary = grade.default_base_pay + (
                grade.custom_dependent_value * (cint(doc.custom_dependent) - 1)
            )
        else:
            doc.custom_net_salary = grade.default_base_pay
        # doc.save()
        frappe.db.commit()


@frappe.whitelist()
def money_in_words(number, main_currency=None, fraction_currency=None):
    """
    Returns string in words with currency and fraction currency.
    """
    from frappe.utils import get_defaults, in_words, get_number_format_info

    _ = frappe._
    # delete the word 'واحد' from the number words if start with 1
    start_in_one_word = str(number).startswith("1")
    try:
        # note: `flt` returns 0 for invalid input and we don't want that
        number = float(number)
    except ValueError:
        return ""

    number = flt(number)
    if number < 0:
        return ""

    d = get_defaults()
    if not main_currency:
        main_currency = d.get("currency", "USD")
    if not fraction_currency:
        fraction_currency = frappe.db.get_value(
            "Currency", main_currency, "fraction", cache=True
        ) or _("Cent")

    number_format = (
        frappe.db.get_value("Currency", main_currency,
                            "number_format", cache=True)
        or frappe.db.get_default("number_format")
        or "#,###.##"
    )

    fraction_length = get_number_format_info(number_format)[2]

    n = "%.{0}f".format(fraction_length) % number

    numbers = n.split(".")
    main, fraction = numbers if len(numbers) > 1 else [n, "00"]

    if len(fraction) < fraction_length:
        zeros = "0" * (fraction_length - len(fraction))
        fraction += zeros

    in_million = True
    if number_format == "#,##,###.##":
        in_million = False

    fraction_currency = _(fraction_currency)
    main_currency = _(main_currency)
    # 0.00
    if main == "0" and fraction in ["00", "000"]:
        out = "{0} {1}".format(main_currency, _("Zero"))
    # 0.XX
    elif main == "0":
        out = _(in_words(fraction, in_million).title()) + \
            " " + fraction_currency
    else:
        out = _(in_words(main, in_million).title()) + " " + main_currency
        if cint(fraction):
            out = (
                out
                + " "
                + _("and")
                + " "
                + _(in_words(fraction, in_million).title())
                + " "
                + fraction_currency
            )

    if start_in_one_word and out[:4] == "واحد":
        out = out[5:]

    out = re.sub(r"(\b\w*ائة)(\w+\b)", r"\1 و \2", out)
    out = re.sub(r"(\b\w*ئتان)(\w+\b)", r"\1 و \2", out)
    # return out + " " + _("only.")
    return out


def check_custom_has_assets(doc, method):
    doc.custom_has_assets = 0
    for row in doc.items:
        if frappe.get_doc("Item", row.item_code).is_fixed_asset:
            doc.custom_has_assets = 1
            break


# Employee Promotion on_submit event.
@frappe.whitelist()
def create_external_work_history(doc, method):
    try:
        if doc.custom_created_by_monthly_promotion == 1:
            work_history = frappe.new_doc("Employee Internal Work History")
            work_history.parent = doc.employee
            work_history.from_date = doc.promotion_date
            work_history.department = doc.department
            work_history.parentfield = "internal_work_history"
            work_history.parenttype = "Employee"
            for row in doc.promotion_details:
                if row.property == "Grade":
                    work_history.custom_grade = row.new

                if row.property == "Designation":
                    work_history.designation = row.new
                else:
                    work_history.designation = doc.custom_currennt_designation

                if row.property == "Dependent":
                    work_history.custom_dependent = row.new

                if row.property == "Branch":
                    work_history.branch = row.new
                else:
                    work_history.branch = doc.custom_branch

            work_history.insert(ignore_permissions=True)
            frappe.db.set_value(
                "Employee Promotion",
                doc.name,
                "custom_internal_work_history",
                work_history.name,
            )
            frappe.db.set_value(
                "Employee",
                doc.employee,
                "custom_last_promotion_date",
                doc.promotion_date,
            )

    except Exception as e:
        frappe.log_error("Error while creating Employee Internal Work History")
        return


# Employee Promotion on_cancel event.
@frappe.whitelist()
def cancel_external_work_history(doc, method):
    if doc.custom_internal_work_history:
        frappe.db.sql(
            f""" DELETE FROM `tabEmployee Internal Work History` WHERE name='{doc.custom_internal_work_history}' """,
            as_dict=True,
        )
        frappe.db.commit()
        frappe.db.set_value("Employee", doc.employee,
                            "custom_last_promotion_date", doc.custom_old_promotion_date)
        # last_pro_date = frappe.get_last_doc(
        #     "Employee Promotion", filters={"employee": doc.employee, "docstatus": 1})
        # if last_pro_date:
        #     frappe.db.set_value(
        #         "Employee",
        #         doc.employee,
        #         "custom_last_promotion_date",
        #         last_pro_date.promotion_date,
        #     )


# Ajax Call for "Loan Application".
@frappe.whitelist()
def get_last_loans(applicant_type, applicant):

    # Employee Advance
    if applicant_type == "Employee":
        applicant_dependent = frappe.db.get_value(
            "Employee", applicant, "custom_dependent"
        )
        last_ea = ""
        last_ea_sql = frappe.db.sql(
            f""" SELECT name  FROM `tabEmployee Advance` WHERE employee = '{applicant}'AND docstatus = 1 ORDER BY posting_date DESC LIMIT 1 """,
            as_dict=1,
        )
        if last_ea_sql:
            last_ea = frappe.get_doc("Employee Advance", last_ea_sql[0].name)

    #  Last Loan(not type Solidarity Fund or Treatment).
    last_loan = ""
    last_loan_reasons = ""
    last_loan_sql = frappe.db.sql(
        f"""SELECT name  FROM `tabLoan` WHERE applicant = '{applicant}' AND (loan_type Not LIKE '%التكافل%' AND loan_type NOT LIKE '%علاج%' AND loan_type NOT LIKE '%صح%ة%' ) ORDER BY posting_date DESC LIMIT 1""",
        as_dict=1,
    )
    if last_loan_sql:
        last_loan = frappe.get_doc("Loan", last_loan_sql[0].name)
        last_loan_reasons = frappe.db.get_value(
            "Loan Application", last_loan.loan_application, "description"
        )

    # Last Solidarity Fund Loan.
    last_sf = ""
    last_sf_reasons = ""
    last_sf_sql = frappe.db.sql(
        f"""SELECT name  FROM `tabLoan` WHERE applicant = '{applicant}' AND docstatus = 1 AND loan_type LIKE '%التكافل%' ORDER BY posting_date DESC LIMIT 1""",
        as_dict=1,
    )
    if last_sf_sql:
        last_sf = frappe.get_doc("Loan", last_sf_sql[0].name)
        last_sf_reasons = frappe.db.get_value(
            "Loan Application", last_sf.loan_application, "description"
        )

    # Last Treatment Loan.
    last_treatment = ""
    last_treatment_reasons = ""
    last_treatment_sql = frappe.db.sql(
        f"""SELECT name  FROM `tabLoan` WHERE applicant = '{applicant}' AND docstatus = 1 AND loan_type LIKE  '%علاج%' OR loan_type LIKE  '%صح%ة%'  ORDER BY posting_date DESC LIMIT 1""",
        as_dict=1,
    )
    if last_treatment_sql:
        last_treatment = frappe.get_doc("Loan", last_treatment_sql[0].name)
        last_treatment_reasons = frappe.db.get_value(
            "Loan Application", last_treatment.loan_application, "description"
        )

    return {
        "applicant_dependent": applicant_dependent,
        "last_ea": last_ea,
        "last_loan": last_loan,
        "last_loan_reasons": last_loan_reasons,
        "last_sf": last_sf,
        "last_sf_reasons": last_sf_reasons,
        "last_treatment": last_treatment,
        "last_treatment_reasons": last_treatment_reasons,
    }


# Additional Salary on validate event.
@frappe.whitelist()
def get_employee_salary_slip(doc, method):
    if doc.docstatus == 0:
        ss_sql = frappe.db.sql(
            f""" SELECT name  FROM `tabSalary Slip` WHERE employee = '{doc.employee}' AND docstatus = 0 AND (start_date <= '{doc.payroll_date}' AND '{doc.payroll_date}' <= end_date ) ORDER BY end_date DESC LIMIT 1""",
            as_dict=True,
        )

        doc.custom_employee_salary_slip = ""
        if ss_sql:
            ss_doc = frappe.get_doc("Salary Slip", ss_sql[0].name)
            doc.custom_employee_salary_slip = ss_doc.name
        else:
            msgprint(_("Can not find employee salary slip"))
            make_property_setter(
                doc,
                "custom_employee_salary_slip",
                "hidden",
                0,
                "Check",
                validate_fields_for_doctype=False,
            )


# Additional Salary on_submit event.
@frappe.whitelist()
def overwrite_salary_slip(doc, method):

    if doc.custom_employee_salary_slip:
        ss_doc = frappe.get_doc("Salary Slip", doc.custom_employee_salary_slip)
        do_not_include_in_total = frappe.db.get_value(
            "Salary Component", doc.salary_component, "do_not_include_in_total"
        )
        if doc.type == "Earning":
            ss_doc.append(
                "earnings",
                {
                    "salary_component": doc.salary_component,
                    "amount": doc.amount,
                    "do_not_include_in_total": do_not_include_in_total,
                },
            )
            ss_doc.save()

        elif doc.type == "Deduction":
            ss_doc.append(
                "deductions",
                {
                    "salary_component": doc.salary_component,
                    "amount": doc.amount,
                    "do_not_include_in_total": do_not_include_in_total,
                },
            )
            ss_doc.save()


# Additional Salary on_cancel event.
@frappe.whitelist()
def cancel_salary_slip_overwrite(doc, method):
    doc.flags.ignore_links = True
    frappe.db.commit()
    doc = frappe.get_doc("Additional Salary", doc.name)
    if (doc.custom_employee_salary_slip):
        if (frappe.get_doc("Salary Slip", doc.custom_employee_salary_slip).docstatus != 1):
            try:
                ss_name = frappe.db.get_value(
                    'Salary Detail', {'additional_salary': doc.name}, ['parent'])
                ss_doc = frappe.get_doc("Salary Slip", ss_name)

                if ss_doc.docstatus == 0:

                    if doc.type == "Earning":
                        for row in ss_doc.earnings:
                            if row.salary_component == doc.salary_component and row.amount == doc.amount:

                                ss_doc.earnings.remove(row)
                                ss_doc.save()
                                frappe.db.commit()

                    elif doc.type == "Deduction":
                        for row in ss_doc.deductions:
                            if row.salary_component == doc.salary_component and row.amount == doc.amount:

                                ss_doc.deductions.remove(row)
                                ss_doc.save()
                            frappe.db.commit()
            except Exception:
                return "Salary Slip"
    return "done"


# Salary Slip on validate event.
@frappe.whitelist()
def check_for_employee_external_advance(doc, method):
    # check for Employee External Loans.
    eea_list = frappe.get_all(
        "Employee External Loans",
        filters={"employee": doc.employee,
                 "status": "Unpaid", "payment_disabled": 0},
    )

    for row in eea_list:
        eea_doc = frappe.get_doc("Employee External Loans", row.name)
        repay_list = frappe.get_all(
            "External Loans Repayment",
            filters={"parent": eea_doc.name, "salary_slip": doc.name},
        )

        if not repay_list:
            # check if Additional Salary already exists.
            ad_list = frappe.get_all(
                "Additional Salary",
                filters={
                    "custom_employee_external_loans": row.name,
                    "docstatus": 1,
                    "custom_employee_salary_slip": doc.name,
                },
            )
            print(ad_list)
            if not ad_list:
                print("in not ad_list")
                # create Additional Salary.
                new_ad = frappe.new_doc("Additional Salary")
                new_ad.employee = eea_doc.employee
                new_ad.employee_name = eea_doc.employee_name
                new_ad.department = eea_doc.department
                new_ad.company = eea_doc.company
                new_ad.payroll_date = doc.start_date
                new_ad.custom_month = doc.custom_month
                new_ad.salary_component = eea_doc.salary_component
                new_ad.custom_employee_external_loans = eea_doc.name

                if eea_doc.remaining_amount < eea_doc.monthly_repayment_amount:
                    new_ad.amount = eea_doc.remaining_amount
                else:
                    new_ad.amount = eea_doc.monthly_repayment_amount

                new_ad.insert(ignore_permissions=True)
                new_ad.submit()

                # add row in External Loans Repayment.
                new_repayment_row = frappe.new_doc("External Loans Repayment")
                new_repayment_row.salary_slip = doc.name
                new_repayment_row.additional_salary = new_ad.name
                new_repayment_row.status = doc.status
                new_repayment_row.amount = new_ad.amount
                new_repayment_row.parent = eea_doc.name
                new_repayment_row.parentfield = "repayment_schedule"
                new_repayment_row.parenttype = "Employee External Loans"
                new_repayment_row.insert(ignore_permissions=True)
                print(new_repayment_row.name)

                frappe.db.set_value(
                    "Additional Salary",
                    new_ad.name,
                    "custom_employee_salary_slip",
                    doc.name,
                )
                doc.validate()
            else:
                print("in ad_list else",)
                for ad in ad_list:
                    # ad_doc = frappe.get_doc("Employee External Loans", ad.custom_employee_external_loans)
                    ad_doc = frappe.get_doc("Additional Salary", ad.name)
                    # new row in External Loans Repayment.
                    new_repayment_row = frappe.new_doc(
                        "External Loans Repayment")
                    new_repayment_row.salary_slip = doc.name
                    new_repayment_row.additional_salary = ad_doc.name
                    new_repayment_row.status = doc.status
                    new_repayment_row.amount = ad_doc.amount
                    new_repayment_row.parent = eea_doc.name
                    new_repayment_row.parentfield = "repayment_schedule"
                    new_repayment_row.parenttype = "Employee External Loans"
                    new_repayment_row.insert(ignore_permissions=True)
                    print(new_repayment_row.name)


# Salary Slip on_submit event.
@frappe.whitelist()
def update_external_advance_on_submit(doc, method):
    repay_list = frappe.get_all(
        "External Loans Repayment", filters={"salary_slip": doc.name}
    )
    if repay_list:
        for row in repay_list:
            # update row status in External Loans Repayment.
            frappe.db.set_value(
                "External Loans Repayment", row.name, "status", doc.status
            )

            # update remaining_amount,paid_amount.
            repay_doc = frappe.get_doc("External Loans Repayment", row.name)
            eea_doc = frappe.get_doc(
                "Employee External Loans", repay_doc.parent)

            new_paid = eea_doc.paid_amount + repay_doc.amount
            new_remain = eea_doc.remaining_amount - repay_doc.amount

            frappe.db.set_value(
                "Employee External Loans",
                eea_doc.name,
                {
                    "paid_amount": new_paid,
                    "remaining_amount": new_remain,
                },
            )

            # update Employee External Loans status.
            if new_remain == 0:
                frappe.db.set_value(
                    "Employee External Loans", eea_doc.name, "status", "Paid"
                )


# Salary Slip on_cancel event.
@frappe.whitelist()
def update_external_advance_on_cancel(doc, method):
    repay_list = frappe.get_all(
        "External Loans Repayment", filters={"salary_slip": doc.name}
    )
    if repay_list:
        for row in repay_list:
            # update row status in External Loans Repayment.
            frappe.db.set_value(
                "External Loans Repayment", row.name, "status", doc.status
            )

            # update remaining_amount,paid_amount.
            repay_doc = frappe.get_doc("External Loans Repayment", row.name)
            eea_doc = frappe.get_doc(
                "Employee External Loans", repay_doc.parent)

            new_paid = eea_doc.paid_amount - repay_doc.amount
            new_remain = eea_doc.remaining_amount + repay_doc.amount

            frappe.db.set_value(
                "Employee External Loans",
                eea_doc.name,
                {
                    "paid_amount": new_paid,
                    "remaining_amount": new_remain,
                },
            )

            # update Employee External Loans status.
            if new_remain == 0:
                frappe.db.set_value(
                    "Employee External Loans", eea_doc.name, "status", "Paid"
                )
            else:
                frappe.db.set_value(
                    "Employee External Loans", eea_doc.name, "status", "Unpaid"
                )

            # cancel Additional Salary.
            ad_doc = frappe.get_doc(
                "Additional Salary", repay_doc.additional_salary)
            ad_doc.cancel()


# Salary Component validate event.
@frappe.whitelist()
def update_component_order(doc, method):
    sd_list = frappe.db.sql(
        f""" select name from `tabSalary Detail` WHERE salary_component = '{doc.name}' """,
        as_dict=True,
    )
    print(sd_list)
    if sd_list:
        for row in sd_list:
            frappe.db.set_value(
                "Salary Detail", row.name, "custom_order", doc.custom_order
            )
            frappe.db.commit()


def set_custom_supplier_group_sequence_field(doc, method):
    english_letters = re.findall(r"[A-Za-z]", doc.supplier_group)

    if not english_letters:
        return

    result = "".join(english_letters)

    # Get the current max number for this letter from existing suppliers
    existing_suppliers = frappe.get_all(
        "Supplier",
        filters={"supplier_group": doc.supplier_group},
        fields=["custom_supplier_group_sequence"],
    )
    max_number = 0
    for supplier in existing_suppliers:
        identifier = str(supplier.custom_supplier_group_sequence)
        if identifier.startswith(result):
            try:
                number = int(identifier[1:])
                max_number = max(max_number, number)
            except ValueError:
                continue

    # Increment the number for the new supplier
    new_number = max_number + 1
    # doc.custom_supplier_group_sequence_field = f"{result}{new_number}"
    frappe.db.set_value(
        "Supplier", doc.name, "custom_supplier_group_sequence", f"{result}{new_number}"
    )
    # frappe.msgprint(str(f"{result}{new_number}"))
    frappe.db.commit()
    doc.reload()


@frappe.whitelist()
def get_address_html(link_doctype, link_name):
    address_name = frappe.db.sql(
        f"""select parent from `tabDynamic Link` where link_doctype = "{link_doctype}" and parenttype = "Address" and link_name = "{link_name}" """)
    if address_name:
        address_doc = frappe.get_doc("Address", address_name[0][0])
        address_html = address_doc.address_line1 + \
            """, \n""" + address_doc.city + """, \n""" + address_doc.country 
        return address_html


@frappe.whitelist()
def get_party_contact(link_doctype, link_name):
    Contact_name = frappe.db.sql(
        f"""select parent from `tabDynamic Link` where link_doctype = "{link_doctype}" and parenttype = "Contact" and link_name = "{link_name}" """)
    if Contact_name:
        Contact_doc = frappe.get_doc("Contact", Contact_name[0][0])
        user = ""
        phone = ""
        if Contact_doc.user:
            user = Contact_doc.user
        if Contact_doc.phone:
            phone = Contact_doc.phone
        elif Contact_doc.mobile_no:
            phone = Contact_doc.mobile_no

        return {"user": user,
                "phone": phone,
                }


@frappe.whitelist()
def create_contract_from_po(source, target=None):
    def set_missing_values(source, target):
        target.document_type = 'Purchase Order'
        target.document_name = source.name
        target.custom_service_value = source.total
        target.custom_tax = source.total_taxes_and_charges
        target.custom_total = source.grand_total
        target.party_type = 'Supplier'
        target.party_name = source.supplier
        sup_doc = frappe.get_doc('Supplier', source.supplier)
        if sup_doc.custom_commercial_register:
            target.custom_second_party_commercial_register = sup_doc.custom_commercial_register

        if sup_doc.custom_registration_date:
            target.custom_second_party_registration_date = sup_doc.custom_registration_date
        
        if sup_doc.custom_classification:
            target.custom_second_party_classification = sup_doc.custom_classification
        
        if sup_doc.custom_license_number:
            target.custom_second_party_id_number = sup_doc.custom_license_number

        address = get_address_html('Supplier', source.supplier)
        if address:
            target.custom_second_party_address_html = address
        contact = get_party_contact('Supplier', source.supplier)
        if contact:
            target.party_user = contact['user']
            target.custom_second_party_phone = contact['phone']
        target.run_method("set_missing_values")

    doc = get_mapped_doc(
        "Purchase Order",
        source,
        {
            "Purchase Order": {
                "doctype": "Contract",
            },
        },
        target,
        set_missing_values,
        )
    return doc

@frappe.whitelist()
def create_contract_from_so(source, target=None):
    def set_missing_values(source, target):
        target.document_type = 'Sales Order'
        target.document_name = source.name
        target.custom_service_value = source.total
        target.custom_tax = source.total_taxes_and_charges
        target.custom_total = source.grand_total
        target.party_type = 'Customer'
        target.party_name = source.customer
        cus_doc = frappe.get_doc('Customer', source.customer)

        if cus_doc.custom_commercial_register:
            target.custom_second_party_commercial_register = cus_doc.custom_commercial_register

        if cus_doc.custom_registration_date:
            target.custom_second_party_registration_date = cus_doc.custom_registration_date
        
        if cus_doc.custom_classification:
            target.custom_second_party_classification = cus_doc.custom_classification
        
        if cus_doc.custom_license_number:
            target.custom_second_party_id_number = cus_doc.custom_license_number

        address = get_address_html('Customer', source.customer)
        if address:
            target.custom_second_party_address_html = address
        contact = get_party_contact('Customer', source.customer)
        if contact:
            target.party_user = contact['user']
            target.custom_second_party_phone = contact['phone']
        
        for row in source.items:
            if row.prevdoc_docname:
                quo_doc = frappe.get_doc('Quotation', row.prevdoc_docname)
                for item in quo_doc.items:
                    if item.prevdoc_doctype == "Opportunity":
                        opp_doc = frappe.get_doc('Opportunity', item.prevdoc_docname)
                        eqf_doc = frappe.get_doc('Equipment Installation Form', opp_doc.custom_equipment_installation_form)
                        if opp_doc.custom_equipment_installation_form:
                            target.custom_equipment_installation_form = opp_doc.custom_equipment_installation_form
                            target.custom_tower = eqf_doc.towers
                            target.custom_branch = eqf_doc.branch
                            target.custom_office = eqf_doc.office
                            print(opp_doc.custom_equipment_installation_form)
                            print(eqf_doc.towers)

                    break
            break
        target.run_method("set_missing_values")

    doc = get_mapped_doc(
        "Sales Order",
        source,
        {
            "Sales Order": {
                "doctype": "Contract",
            },
        },
        target,
        set_missing_values,
        )
    return doc

@frappe.whitelist()
def create_equipment_installation_from_so(source, target=None):
    def set_missing_values(source, target):
        target.owned_by = source.customer
        # contract_doc = frappe.get_doc('Contact', source.custom_contract)
        # if contract_doc:
        #     target.contract_end_date = contract_doc.end_date
        target.run_method("set_missing_values")
    
    doc = get_mapped_doc(
        "Sales Order",
        source,
        {
            "Sales Order": {
                "doctype": "Equipment Installation",
            },
        },
        target,
        set_missing_values,
        )
    return doc

# Building Accessories
@frappe.whitelist()
def add_building_accessories(doc, method):
    if doc.custom_is_a_building_accessories == 1:
        new_doc = frappe.new_doc("Building Accessories")
        new_doc.asset = doc.name
        new_doc.item_code = doc.item_code
        new_doc.item_name = doc.item_name
        new_doc.parent = doc.custom_buildings 
        new_doc.parentfield = 'building_accessories'
        new_doc.parenttype = 'Buildings'
        new_doc.insert(ignore_permissions=True)

@frappe.whitelist()     
def cancel_building_accessories(doc, method):
    frappe.db.sql(f""" DELETE FROM `tabBuilding Accessories` WHERE asset = '{doc.name}' """)

@frappe.whitelist()
def get_qualification(qualification_template):
    qt_doc = frappe.get_doc('Qualification Template', qualification_template)
    q_list = []
    for item in qt_doc.qualification_template_table:
        q_list.append(item.qualification)
    return {"q_list":q_list}

@frappe.whitelist()
def send_qualification_notification(doc_name, status):
    users = frappe.db.sql(
            f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE role = 'Tower Management' AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
    if users:
        for user in users:
            new_doc = frappe.new_doc("Notification Log")
            new_doc.from_user = frappe.session.user
            new_doc.for_user = user.parent
            new_doc.type = "Share"
            new_doc.document_type = "Lead"
            new_doc.document_name = doc_name
            new_doc.subject = f"""Lead related to Equipment Installation is: {status}"""
            new_doc.email_content = "empty@empty.com"
            new_doc.insert(ignore_permissions=True)
    return "done"

@frappe.whitelist()
def get_pricing_matrix(tower_type):
    tt_doc = frappe.get_doc('Tower Type', tower_type)
    radius_list = []
    height_list = []
    for row in tt_doc.pricing_matrix:
        if row.equipment_radius > 0:
            radius_list.append(row.equipment_radius)

        if row.equipment_height > 0:
            height_list.append(row.equipment_height)

    return {
            "radius_list":radius_list,
            "height_list":height_list,
            }

@frappe.whitelist()
def get_price_for_radius(tower_type,custom_equipment_radius_):
    tt_doc = frappe.get_doc('Tower Type', tower_type)
    price = 0
    height= 0
    for row in tt_doc.pricing_matrix:
        if row.equipment_radius == float(custom_equipment_radius_):
            price += row.price
            if row.equipment_height > 0:
                height += row.equipment_height
           
            
            break

    return {
            "price":price,
            "height":height,
            }

@frappe.whitelist()
def get_price_for_height(tower_type,custom_equipment_height):
    tt_doc = frappe.get_doc('Tower Type', tower_type)
    price = 0
    radius= 0
    for row in tt_doc.pricing_matrix:
        if row.equipment_height== float(custom_equipment_height):
            price += row.price
            if row.equipment_radius > 0:
                radius += row.equipment_radius
           
            
            break

    return {
            "price":price,
            "radius":radius,
            }

@frappe.whitelist()
def create_opportunity_from_lead(source, target=None,owner=None):
    def set_missing_values(source, target):
        target.opportunity_from = "Customer"
        target.party_name = source.customer
        target.source = "Existing Customer"
        target.custom_equipment_installation_form = source.custom_equipment_installation_form_doctype
        target.opportunity_owner = owner
        target.custom_equipment_installation = 1
        target.custom_towers = source.custom_towers
        target.run_method("set_missing_values")

    doc = get_mapped_doc(
        "Lead",
        source,
        {
            "Lead": {
                "doctype": "Opportunity",
            },
        },
        target,
        set_missing_values,
        )
    return doc

@frappe.whitelist()
def update_cost_center_on_submit(doc, method):
    if doc.purpose == "Transfer":
        for row in doc.assets:
            if row.custom_from_cost_center and row.custom_to_cost_center:
                frappe.db.set_value('Asset', row.asset, 'cost_center', row.custom_to_cost_center)
            if row.source_location and row.target_location:
                frappe.db.set_value('Asset', row.asset, 'location', row.target_location)
    print("update_cost_center_on_submit")

@frappe.whitelist()
def update_cost_center_on_cancel(doc, method):
    if doc.purpose == "Transfer":
        for row in doc.assets:
            if row.custom_from_cost_center and row.custom_to_cost_center:
                frappe.db.set_value('Asset', row.asset, 'cost_center', row.custom_from_cost_center)
            if row.source_location and row.target_location:
                frappe.db.set_value('Asset', row.asset, 'location',row.source_location)
    print("update_cost_center_on_cancel")

@frappe.whitelist()
def update_realty_available_area_on_submit(doc, method):
    if doc.custom_realty == 1 :
        if doc.custom_realty_name and (doc.custom_needed_space > 0) :
            realty_doc = frappe.get_doc('Realty', doc.custom_realty_name)
            new_available_space = float(realty_doc.available_area) - doc.custom_needed_space
            frappe.db.set_value('Realty', doc.custom_realty_name, 'available_area', float(new_available_space))

    print("update_realty_available_area_on_submit")

@frappe.whitelist()
def update_realty_available_area_on_cancel(doc, method):
    if doc.custom_realty == 1 :
        if doc.custom_realty_name and (doc.custom_needed_space > 0) :
            realty_doc = frappe.get_doc('Realty', doc.custom_realty_name)
            new_available_space = float(realty_doc.available_area) + doc.custom_needed_space
            frappe.db.set_value('Realty', doc.custom_realty_name, 'available_area', float(new_available_space))
            
    print("update_realty_available_area_on_cancel")

@frappe.whitelist()
def send_opportunity_notification(doc_name):
    users = frappe.db.sql(
            f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'Sales Manager' or role = 'Commercial Management') AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
    if users:
        for user in users:
            new_doc = frappe.new_doc("Notification Log")
            new_doc.from_user = frappe.session.user
            new_doc.for_user = user.parent
            new_doc.type = "Share"
            new_doc.document_type = "Opportunity"
            new_doc.document_name = doc_name
            new_doc.subject = f"""Opportunity validated"""
            new_doc.email_content = "empty@empty.com"
            new_doc.insert(ignore_permissions=True)
    return "done"

@frappe.whitelist()
def send_quotation_notification(doc_name):
    users = frappe.db.sql(
            f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'Sales Manager' or role = 'Commercial Management' or role ='Contracts Unit Employee') AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
    if users:
        for user in users:
            new_doc = frappe.new_doc("Notification Log")
            new_doc.from_user = frappe.session.user
            new_doc.for_user = user.parent
            new_doc.type = "Share"
            new_doc.document_type = "Quotation"
            new_doc.document_name = doc_name
            new_doc.subject = f"""Quotation Submitted"""
            new_doc.email_content = "empty@empty.com"
            new_doc.insert(ignore_permissions=True)
    return "done"


@frappe.whitelist()
def send_so_notification(doc_name):
    users = frappe.db.sql(
            f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'Sales Manager' or role = 'Commercial Management' or role ='Contracts Unit Employee' or role = 'General Management') AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
    if users:
        for user in users:
            new_doc = frappe.new_doc("Notification Log")
            new_doc.from_user = frappe.session.user
            new_doc.for_user = user.parent
            new_doc.type = "Share"
            new_doc.document_type = "Sales Order"
            new_doc.document_name = doc_name
            new_doc.subject = f"""Sales Order Submitted"""
            new_doc.email_content = "empty@empty.com"
            new_doc.insert(ignore_permissions=True)
    return "done"


@frappe.whitelist()
def send_contract_notification(doc_name):
    users = frappe.db.sql(
            f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'Sales Manager' or role = 'Commercial Management' or role ='Contracts Unit Employee' or role = 'Technical Management') AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
    if users:
        for user in users:
            new_doc = frappe.new_doc("Notification Log")
            new_doc.from_user = frappe.session.user
            new_doc.for_user = user.parent
            new_doc.type = "Share"
            new_doc.document_type = "Contract"
            new_doc.document_name = doc_name
            new_doc.subject = f"""Contract Submitted"""
            new_doc.email_content = "empty@empty.com"
            new_doc.insert(ignore_permissions=True)
    return "done"

