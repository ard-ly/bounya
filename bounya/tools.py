# -*- coding:utf-8 -*-
# encoding: utf-8

# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import frappe, os
from frappe.model.document import Document
from frappe.utils.data import flt, nowdate, getdate, cint
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate, add_years
from datetime import date


def update_employee_retirement_date():
    retirement_age_male = flt(frappe.db.get_single_value("HR Settings", "retirement_age")) or 0.0
    retirement_age_female = flt(frappe.db.get_single_value("HR Settings", "custom_retirement_age_female")) or 0.0

    emps = frappe.db.sql_list("select name from `tabEmployee` where status='Active'")
    for emp in emps:
        retirement_age = 0.0

        doc = frappe.get_doc("Employee", emp)
        if doc.gender=='Male' and retirement_age_male>0:
            retirement_age = retirement_age_male
        elif doc.gender=='Female' and retirement_age_female>0:
            retirement_age = retirement_age_female

        retirement_date = add_years(doc.date_of_birth, retirement_age)

        if getdate(doc.date_of_retirement)!=getdate(retirement_date):
            doc.date_of_retirement = getdate(retirement_date)
            doc.flags.ignore_mandatory = True
            doc.save(ignore_permissions=True)

            print(f"* update date of retirement for employee: {doc.name}")



def increase_employee_monthly_leave_balance():
    annual_leave = frappe.get_value("Leave Type", filters = {"custom_is_annual_leave": 1}, fieldname = "name") or None

    if annual_leave:
        emps = frappe.get_all("Employee",filters = {"status": "Active"}, fields = ["name", "date_of_birth"])
        for emp in emps:
            allocation = frappe.db.sql(f"select name from `tabLeave Allocation` where leave_type='{annual_leave}' and employee='{emp.name}' and '{nowdate()}' between from_date and to_date order by to_date desc limit 1", as_dict=True)
            if allocation:
                allocation_name = allocation[0].get("name")

                monthly_leave_balance = 2.5

                employee_age = int(get_age(emp.date_of_birth))

                if employee_age>50:
                    monthly_leave_balance = 3.75
                    
                print(employee_age)
                
                # doc = frappe.get_doc('Leave Allocation', allocation_name)
                # leave_balance = doc.new_leaves_allocated + 2.5
                # doc.new_leaves_allocated = leave_balance
                # doc.total_leaves_allocated = doc.unused_leaves+leave_balance
                # doc.save()

                # print("Increase monthly leave balance for employee: {0}".format(emp.name))



# Get age of inserted date
def get_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


