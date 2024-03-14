import json

import frappe
from erpnext.controllers.status_updater import validate_status
from frappe.utils import getdate
from frappe.permissions import remove_user_permission
from frappe.model.naming import set_name_by_naming_series
from erpnext.setup.doctype.employee.employee import Employee, InactiveEmployeeStatusError
from frappe import _, throw
import re
from frappe.utils import getdate, cint
from datetime import datetime
from frappe.query_builder import Order
from frappe.query_builder.functions import Sum
from frappe.utils import (
	add_days,
	ceil,
	cint,
	cstr,
	date_diff,
	floor,
	flt,
	formatdate,
	get_first_day,
	get_link_to_form,
	getdate,
	money_in_words,
	rounded,
)

@frappe.whitelist()
def fetch_addetionl_fraction( additionl_type):
    fraction = frappe.get_value("Additional Salary Setting" , additionl_type , "fraction_of_hourly_salary_for_additional_work")
    return fraction

@frappe.whitelist()
def fetch_addetionl_component():
    settings = frappe.get_doc('Payroll Settings')
    component = settings.custom_addational_salary_component
    return component

@frappe.whitelist()
def check_sal_struct(employee, date):

    joining_date, relieving_date = frappe.get_cached_value(
        "Employee", employee, ("date_of_joining", "relieving_date")
    )
    ss = frappe.qb.DocType("Salary Structure")
    ssa = frappe.qb.DocType("Salary Structure Assignment")

    query = (
        frappe.qb.from_(ssa)
        .join(ss)
        .on(ssa.salary_structure == ss.name)
        .select(ssa.salary_structure , ssa.base)
        .where(
            (ssa.docstatus == 1)
            & (ss.docstatus == 1)
            & (ss.is_active == "Yes")
            & (ssa.employee == employee)
            & (
                (ssa.from_date <= date)
                | (ssa.from_date <= date)
                | (ssa.from_date <= joining_date)
            )
        )
        .orderby(ssa.from_date, order=Order.desc)
        .limit(1)
    )
    st_name = query.run()
    settings = frappe.get_doc('Payroll Settings')
    hour_base = settings.custom_defulte_working_days * settings.custom_defulte_working_hours
    if st_name and hour_base:
        # salary_structure = st_name[0][0]
        base = st_name[0][1]
        print(":::::::::::::::::::::::::::" , base)
        return (base / hour_base )
    else:
        return 0 

    # else:
    #     salary_structure = None
    #     frappe.msgprint(
    #         _("No active or default Salary Structure found for employee {0} for the given dates").format(
    #             employee
    #         ),
    #         title=_("Salary Structure Missing"),
    #     )