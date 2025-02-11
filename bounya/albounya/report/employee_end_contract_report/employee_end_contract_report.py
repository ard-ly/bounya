# encoding: utf-8
# Copyright (c) 2025, ARD Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, getdate, flt, add_days, add_months, get_last_day, date_diff, nowdate, add_years
from datetime import datetime, date
import datetime


def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_columns(filters):
    return [
        _("Employee") + ":Link/Employee:150",
        _("Employee Name") + "::200",
        _("Date of Joining") + ":Date:150",
        _("Contract Duration") + "::150",
        _("Contract End Date") + ":Date:150",
        _("Days Remaining") + "::150"
        ]


def get_conditions(filters):
    conditions = ""

    if filters.get("employee"): conditions += " and employee = '{0}'".format(filters.get("employee"))
    
    return conditions


def get_data(filters):
    data = []
    conditions = get_conditions(filters)
    li_list=frappe.db.sql("""select employee, employee_name, date_of_joining, custom_contract_duration from `tabEmployee` where status='Active' and custom_contract_type='محدد المدة' and custom_contract_duration!='دائم' {0} order by date_of_birth asc""".format(conditions), as_dict=1)
    
    for emp in li_list:
        contract_end_date = emp.date_of_joining

        if emp.custom_contract_duration=='سنة':
            contract_end_date = add_years(emp.date_of_joining, 1)
        elif emp.custom_contract_duration=='ستة أشهر':
            contract_end_date = add_months(emp.date_of_joining, 6)

        days_left = (getdate(contract_end_date) - getdate(nowdate())).days
        days_left = "عقد منتهي" if days_left <= 0 else days_left

        row = [
            emp.employee,
            emp.employee_name,
            emp.date_of_joining,
            emp.custom_contract_duration,
            contract_end_date,
            days_left,
        ]

        data.append(row)


    return data


