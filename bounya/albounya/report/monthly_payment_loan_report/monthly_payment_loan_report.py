# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe import get_query
from frappe.query_builder.functions import Extract

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Employee Number"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options":"Employee",
			"width": 100,
		},
		{
			"label": _("Full Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Link",
			"options":"Branch",
			"width": 100,
		},
		{
			"label": _("Net Salary"),
			"fieldname": "net_pay",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("Loan Type"),
			"fieldname": "loan_type",
			"fieldtype": "Link",
			"options": "Loan Type",
			"width": 200,
		},
		{
			"label": _("Loan Amount"),
			"fieldname": "loan_amount",
			"fieldtype": "Currency",
			"options": "Loan Type",
			"width": 200,
		}, 
		{
			"label": _("Total Principal Paid"),
			"fieldname": "total_principal_paid",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("Total Principal Amount"),
			"fieldname": "principal_amount",
			"fieldtype": "Currency",
			"width": 200,
		},
 
		{
			"label": _("Salary Slip"),
			"fieldname": "n",
			"fieldtype": "Link",
			"options": "Salary Slip" ,
			"width": 200,
		},
 
	 	]

# def get_data(filters=None):
# 	conditions = []
# 	ss = frappe.qb.DocType("Salary Slip")
# 	sl = frappe.qb.DocType("Salary Slip Loan")
# 	l = frappe.qb.DocType("Loan")
# 	# salary_detail = frappe.qb.DocType("Salary Detail")
# 	# salary_component = frappe.qb.DocType("Salary Component")
# 	# employee = frappe.qb.DocType("Employee")
# 	# query = get_query("Salary Slip", ss)
# 	query = (frappe.qb.from_(ss).select(ss.star))
# 	# Add base condition
# 	conditions.append(ss.status == "Submitted")

# 	# Add filters based on provided arguments
# 	if filters.get("company"):
# 		conditions.append(ss.company.isin(filters.get("company")))  # Use IN for multiple companies
# 	if filters.get("employee"):
# 		conditions.append(ss.employee == filters.get("employee"))
# 	if filters.get("from_date"):
# 		conditions.append(ss.start_date >= filters.get("from_date"))
# 	if filters.get("to_date"):
# 		conditions.append(ss.end_date <= filters.get("to_date"))
# 	# Add filter for employee name (if needed)
# 	# if filters.get("employee_name"):
# 	#   conditions.append(ss.employee_name.like("%{}%".format(filters.get("employee_name"))))
# 	if filters.get("branch"):
# 		conditions.append(ss.branch == filters.get("branch"))

# 	query = query.filter(*conditions)

# 	# Join tables and select required fields
# 	query = query.join("Salary Slip Loan", "sl", on=(sl.parent == ss.name))
# 	query = query.join("Loan", "l", on=(sl.loan == l.name))
# 	query = query.select(ss.name.as_("n"), ss.start_date, ss.end_date, ss.total_principal_amount, l.interest_rate, *ss)

# 	return query.run(as_dict=True)


# def get_data(filters=None):


# 	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}
# 	SalarySlip = frappe.qb.DocType("Salary Slip")
# 	SalaryDetail = frappe.qb.DocType("Salary Detail")
# 	salary_slip = frappe.qb.DocType("Salary Slip")
# 	sl = frappe.qb.DocType("Salary Slip Loan")
# 	l = frappe.qb.DocType("Loan")

# 	# query = frappe.qb.from_(salary_slip).left_join(employee).on(employee.name == salary_slip.name).select(salary_slip.star)
# 	query = (frappe.qb.from_(salary_slip).select(salary_slip.star))
# 			# .inner_join("Salary SLip Loan")
# 			# .on(sl.parent == salary_slip.name)
# 			# .inner_join("Loan")
# 			# .on(sl.loan == l.name)
# 			# .select(salary_slip.name.as_("n"), salary_slip.start_date, salary_slip.end_date, salary_slip.total_principal_amount, l.interest_rate, *salary_slip))

# 	if filters.get("docstatus"):
# 		query = query.where(salary_slip.docstatus == doc_status[filters.get("docstatus")])

# 	if filters.get("from_date"): 
# 		query = query.where(salary_slip.start_date >= filters.get("from_date"))

# 	if filters.get("to_date"):
# 		query = query.where(salary_slip.end_date <= filters.get("to_date"))

# 	if filters.get("company"):
# 		query = query.where(salary_slip.company == filters.get("company"))

# 	if filters.get("employee"):
# 		query = query.where(salary_slip.employee == filters.get("employee"))

# 	if filters.get("branch"):
# 		query = query.where(salary_slip.branch == filters.get("branch"))
	

# 	# if filters.get("month"):
# 	# 	query = query.where(Extract("month", salary_slip.start_date) == filters.month)
# 	salary_slips = query.run(as_dict=1)

# 	return salary_slips or []


def get_data(filters=None):
	conditions = get_conditions(filters)

	slips = frappe.db.sql("""
				SELECT ss.name n, ss.start_date start_date , ss.end_date end_date , ss.*, sl.*  , sl.principal_amount   principal_amount , l.*   
					FROM `tabSalary Slip` ss
					INNER JOIN  `tabSalary Slip Loan` sl ON sl.parent = ss.name
					INNER JOIN `tabLoan` l	ON sl.loan = l.name
					{}
					   """.format(conditions), as_dict=True)

	# slips = frappe.db.sql("""
	# 			SELECT ss.employee , ss.employee_name, emp.custom_bank_name, emp.bank_ac_no , emp.custom_employee_bank_branch , ss.net_pay , emp.custom_national_number, emp.branch
	# 	    	FROM `tabSalary Slip` ss
	# 			LEFT JOIN `tabEmployee` emp ON ss.employee=emp.name
	# 	       	{}
	# 		""".format(conditions), as_dict=True)
	return slips

def get_conditions(filters):
	conditions = ["ss.status!='Cancale' "]

	if filters.get("company"):
		conditions.append("ss.company='{}'".format(filters.get("company")))

	if filters.get("employee"):
		conditions.append("ss.employee='{}'".format(filters.get("employee")))

	if filters.get("from_date"):
		conditions.append("ss.start_date >= '{}'".format(filters.get("from_date")))

	if filters.get("to_date"):
		conditions.append("ss.end_date <= '{}'".format(filters.get("to_date")))

	if filters.get("loan_type"):
		conditions.append("sl.loan_type = '{}'".format(filters.get("loan_type")))

	if filters.get("branch"):
		conditions.append("ss.branch='{}'".format(filters.get("branch")))

	return " WHERE " + " AND ".join(conditions)
