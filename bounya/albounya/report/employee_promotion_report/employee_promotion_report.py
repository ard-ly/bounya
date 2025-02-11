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
        _("Last Promotion Date") + ":Date:150",
        _("Next Promotion Date") + ":Date:150",
        _("Late Promotion Days") + "::150"
        ]


def get_conditions(filters):
    conditions = ""

    if filters.get("employee"): conditions += " and employee = '{0}'".format(filters.get("employee"))
    
    return conditions


def get_data(filters):
    data = []
    conditions = get_conditions(filters)
    li_list=frappe.db.sql("""select employee, employee_name, date_of_joining, custom_contract_type from `tabEmployee` where status='Active' {0} order by date_of_joining desc""".format(conditions), as_dict=1)
    
    for emp in li_list:
        promotion_period_years = 0
        late_days = 0

        hr_settings = frappe.get_single("HR Settings")
        if hr_settings.custom_employee_promotion_settings:
            for row in hr_settings.custom_employee_promotion_settings:
                if row.contract_type == emp.custom_contract_type:
                    promotion_period_years = row.promotion_after_years
                    break

        if emp.custom_contract_type and promotion_period_years>0:
            previous_promotion_date = getdate(emp.date_of_joining)

            last_employee_promotion_entry = frappe.db.sql("""
                SELECT promotion_date 
                FROM `tabEmployee Promotion` 
                WHERE employee = %s AND docstatus = 1
                ORDER BY promotion_date DESC
                LIMIT 1
            """, (emp.employee), as_dict=True)
            if last_employee_promotion_entry:
                previous_promotion_date = last_employee_promotion_entry[0].promotion_date

            next_promotion_date = add_years(getdate(previous_promotion_date), promotion_period_years)

            days_left = (getdate(next_promotion_date) - getdate(nowdate())).days

            remaining_days = date_diff(getdate(next_promotion_date), getdate(nowdate))
            if remaining_days < 0:
                late_days = abs(remaining_days)
                
            row = [
                emp.employee,
                emp.employee_name,
                emp.date_of_joining,
                previous_promotion_date,
                next_promotion_date,
                late_days
            ]

            data.append(row)


    return data


