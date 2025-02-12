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
        _("Leave Type") + ":Link/Leave Type:150",
        _("From Date") + ":Date:150",
        _("To Date") + ":Date:150",
        _("Return Date") + ":Date:150",
        _("Days Remaining") + "::150"
        ]


def get_conditions(filters):
    conditions = ""

    if filters.get("employee"): conditions += " and employee = '{0}'".format(filters.get("employee"))
    
    return conditions


def get_data(filters):
    data = []
    conditions = get_conditions(filters)
    li_list=frappe.db.sql("""select employee, employee_name, leave_type, from_date, to_date from `tabLeave Application` where docstatus=1 and leave_type='اجازة بدون مرتب' {0} order by creation desc""".format(conditions), as_dict=1)
    
    for leave in li_list:
        return_date = getdate(add_days(leave.to_date, 1))

        days_remaining = date_diff(getdate(return_date), getdate(nowdate))

        if days_remaining>0:
            row = [
                leave.employee,
                leave.employee_name,
                leave.leave_type,
                leave.from_date,
                leave.to_date,
                return_date,
                days_remaining
            ]

            data.append(row)


    return data


