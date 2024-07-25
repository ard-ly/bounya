# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	conditions = get_conditions(filters)
	columns, data =  get_columns(), get_data(conditions)
	return columns, data

def get_columns():
    columns = [
        {
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
        },
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
        },
        {
            "label": _("Type"),
            "fieldname": "type",
            "fieldtype": "Link",
            "options": "External Loans Type",
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
        },
        {
            "label": _("Advance Amount"),
            "fieldname": "advance_amount",
            "fieldtype": "Currency",
            "options": "currency",
        }, 
        {
            "label": _(" Monthly Repayment Amount "),
            "fieldname": "monthly_repayment_amount",
            "fieldtype": "Currency",
            "options": "currency",
        },
        {
            "label": _("Total Paid Amount"),
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "options": "currency",
        },
        {
            "label": _("Remaining Amount"),
            "fieldname": "remaining_amount",
            "fieldtype": "Currency",
            "options": "currency",
        },
	]
    return columns

def get_data(conditions):
    data = frappe.db.sql(
        f"""SELECT employee,employee_name,department,type,status,advance_amount,paid_amount,remaining_amount , monthly_repayment_amount FROM `tabEmployee External Loans` {conditions}""", as_dict=True)
    
    return data

def get_conditions(filters):
    conditions = " WHERE docstatus=1"
    employee = filters.get("employee")
    department = filters.get("department") 
    status = filters.get("status")
    type = filters.get("type")
       
    if employee:
        conditions += " AND employee = '{0}' ".format(employee)
    if department:
          conditions += " AND department = '{0}' ".format(department)
    if status:
          conditions += " AND status = '{0}' ".format(status)
    if type:
          conditions += " AND type = '{0}' ".format(type)
   
    print(conditions)
	
    return conditions