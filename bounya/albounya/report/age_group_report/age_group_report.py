# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff
from frappe.utils import today
# Import math library
import math

def execute(filters=None):
	conditions = get_conditions(filters)
	columns, data =  get_columns(), get_data(conditions)
	return columns, data

def get_columns():
    columns = [
        {
            "label": _("Employee"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": "250"
        },
			{
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": "150"
        },

        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": "150"
        },
		{
            "label": _("Date of Birth"),
            "fieldname": "date_of_birth",
            "fieldtype": "Date",
            "width": "150"
        },
		{
            "label": _("Age (years)"),
            "fieldname": "age_year",
            "fieldtype": "Int",
            "width": "120"
        }, 
		{
            "label": _("Age (Month)"),
            "fieldname": "age_month",
            "fieldtype": "Float",
            "width": "120"
        }, 
		{
            "label": _("Age Group"),
            "fieldname": "age_group",
            "fieldtype": "Data",
            "width": "120"
        }, 

	]
    return columns



def get_data(conditions):
	data = frappe.db.sql(
		f"""SELECT name,employee_name,department,branch ,status  ,date_of_birth FROM `tabEmployee` {conditions}""", as_dict=True)
	for d in data:
		age_year  = math.ceil(date_diff( today() , d.date_of_birth)/365.25)
		age_month = date_diff( today() , d.date_of_birth)/365.25
		d.update({'age_year': age_year})
		d.update({'age_month': age_month})

		if age_year < 25:
			d.update({'age_group': "< 25 "})

		elif age_year >= 25 and age_year < 36 :
			d.update({'age_group': "25 - 35"})
	
		elif age_year >= 36 and age_year < 46 :
			d.update({'age_group': "36 - 45 "})
	
		elif age_year >= 46 and age_year < 56 :
			d.update({'age_group': "46 - 55"})	

		elif age_year >= 56 and age_year < 65 :
			d.update({'age_group': "56 - 65"})
		else:
			d.update({'age_group': "> 65"})
	
			
	return data

def get_conditions(filters):
    conditions = " WHERE 1=1"
    employee = filters.get("employee")
    branch = filters.get("branch") 
    status = filters.get("status")
    type = filters.get("type")
       
    if employee:
        conditions += " AND employee = '{0}' ".format(employee)
    if branch:
          conditions += " AND branch = '{0}' ".format(branch)
    if status:
          conditions += " AND status = '{0}' ".format(status)
    if type:
          conditions += " AND type = '{0}' ".format(type)
   
    print(conditions)
	
    return conditions