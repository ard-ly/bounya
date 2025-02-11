# encoding: utf-8
# Copyright (c) 2025, ARD Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, getdate, flt, add_days, add_months, get_last_day, date_diff, nowdate
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
        _("Retirement Age") + "::150",
        _("Retirement Date") + ":Date:150",
        _("Days Remaining") + "::150"
        ]


def get_conditions(filters):
    conditions = ""

    if filters.get("employee"): conditions += " and employee = '{0}'".format(filters.get("employee"))
    
    return conditions


def get_data(filters):
    data = []
    conditions = get_conditions(filters)
    li_list=frappe.db.sql("""select employee, employee_name, date_of_joining, gender, date_of_retirement from `tabEmployee` where status='Active' {0} order by date_of_birth asc""".format(conditions), as_dict=1)
    
    for emp in li_list:
        retirement_age = 65 
        if emp.gender == 'Male':
            retirement_age = frappe.db.get_value("HR Settings", "HR Settings", "retirement_age")
        elif emp.gender == 'Female':
            retirement_age = frappe.db.get_value("HR Settings", "HR Settings", "custom_retirement_age_female")

        days_remaining = date_diff(getdate(emp.date_of_retirement), getdate(nowdate))

        if days_remaining>0 and days_remaining<=90:
            row = [
                emp.employee,
                emp.employee_name,
                emp.date_of_joining,
                retirement_age,
                emp.date_of_retirement,
                days_remaining
            ]

            data.append(row)


    return data


