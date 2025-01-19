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


