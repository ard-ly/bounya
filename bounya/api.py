import re
import frappe
from datetime import date
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, today
from frappe.utils.data import money_in_words
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
        frappe.db.get_value("Currency", main_currency, "number_format", cache=True)
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
        out = _(in_words(fraction, in_million).title()) + " " + fraction_currency
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

                if row.property == "Dependent":
                    work_history.custom_dependent = row.new

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
        last_pro_date = frappe.get_last_doc(
            "Employee Promotion", filters={"employee": "HR-EMP-00002", "docstatus": 1}
        )
        # frappe.db.sql(f""" SELECT promotion_date  FROM `tabEmployee Promotion` WHERE employee = '{doc.employee}' AND docstatus =1 ORDER BY promotion_date DESC LIMIT 1 """,as_dict=True)
        if last_pro_date:
            frappe.db.set_value(
                "Employee",
                doc.employee,
                "custom_last_promotion_date",
                last_pro_date.promotion_date,
            )

        else:
            frappe.db.set_value(
                "Employee", doc.employee, "custom_last_promotion_date", " "
            )


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


@frappe.whitelist()
def cancel_salary_slip_overwrite(doc, method):
        
        doc = frappe.get_doc("Additional Salary", doc.name)
        if doc.custom_employee_salary_slip:
            try :
                ss_doc = frappe.get_doc("Salary Slip", doc.custom_employee_salary_slip)
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
    eea_list = frappe.get_list(
        "Employee External Loans",
        filters={"employee": doc.employee, "status": "Unpaid", "payment_disabled": 0},
    )

    for row in eea_list:
        eea_doc = frappe.get_doc("Employee External Loans", row.name)
        repay_list = frappe.get_list(
            "External Loans Repayment",
            filters={"parent": eea_doc.name, "salary_slip": doc.name},
        )

        if not repay_list:
            # check if Additional Salary already exists.
            ad_list = frappe.get_list(
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
            else:
                print("in ad_list else")
                for ad in ad_list:
                    ad_doc = frappe.get_doc("Employee External Loans", ad.name)
                    # new row in External Loans Repayment.
                    new_repayment_row = frappe.new_doc("External Loans Repayment")
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
    repay_list = frappe.get_list(
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
            eea_doc = frappe.get_doc("Employee External Loans", repay_doc.parent)

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
    repay_list = frappe.get_list(
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
            eea_doc = frappe.get_doc("Employee External Loans", repay_doc.parent)

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
            ad_doc = frappe.get_doc("Additional Salary", repay_doc.additional_salary)
            ad_doc.cancel()


# Salary Component validate event.
@frappe.whitelist()
def update_component_order(doc, method):
    sd_list = frappe.db.sql(
        f""" select name from `tabSalary Detail` WHERE salary_component = '{doc.salary_component}' """,
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
