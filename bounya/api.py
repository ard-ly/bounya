

import re

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt

import erpnext
# from scipy import interpolate
# from scipy.interpolate import CubicSpline

@frappe.whitelist()
def make_demo_data(doc ,salary_structure ,marital_status, number_of_children , base , evaluation , performance_factor):
	try:
		employee =  frappe.new_doc("Employee")
		employee.first_name = "Demo"
		employee.gender = 'Male'
		employee.date_of_birth = '1990-01-01'
		employee.date_of_joining = '2020-01-01'
		employee.holiday_list = 'h1'
		# employee.marital_status = 'Married'
		employee.marital_status = marital_status
		employee.custom_number_of_children = number_of_children
		employee.insert()

		# calculate family and housing
		if employee.marital_status == 'Single':
			family_allowance = 0
			housing_allowance = 100
		elif employee.marital_status == 'Married' and employee.custom_number_of_children == 1 :
			family_allowance = 200
			housing_allowance = 200
		elif employee.marital_status == 'Married' and employee.custom_number_of_children != 1 :
			family_allowance = 100
			housing_allowance = 150	

		# salary_structure = 'st1'
		salary_structure_assignment = frappe.new_doc('Salary Structure Assignment')
		salary_structure_assignment.employee = employee.name
		salary_structure_assignment.salary_structure = salary_structure
		salary_structure_assignment.from_date = '2023-01-01'
		salary_structure_assignment.custom_evaluation = evaluation
		salary_structure_assignment.custom_performance_factor = performance_factor
		salary_structure_assignment.custom_family_allowance = family_allowance
		salary_structure_assignment.custom_housing_allowance = housing_allowance
		salary_structure_assignment.base = base
		salary_structure_assignment.insert()
		salary_structure_assignment.submit()

		salary_slip = frappe.new_doc("Salary Slip")
		salary_slip.employee = employee.name
		salary_slip.posting_date = '2024-01-01'
		# salary_slip.salary_structure = salary_structure
		salary_slip.insert()
		salary_slip.employee = ""
		salary_slip.employee = employee.name
		salary_slip.save()
		net_pay = salary_slip.net_pay

		# delete transection sample data
		frappe.delete_doc("Salary Slip" , salary_slip.name)
		salary_structure_assignment.cancel()
		frappe.delete_doc("Salary Structure Assignment" , salary_structure_assignment.name)
		frappe.delete_doc("Employee" , employee.name)
		# print("Salary Net gross : " , salary_slip.net_pay)
		return base , net_pay
	except Exception as e:
		msg = _(e)
		frappe.throw(msg, title=_("Payment Unlink Error"))
		frappe.msgprint(e)
	
@frappe.whitelist()
def calculate_interpolate_value(doc , employee_no , salary_structure , custom_net_salary , evaluation):
	salary_structure = frappe.get_doc("Salary Structure" ,salary_structure)
	employee = frappe.get_doc("Employee" , employee_no)

	# test_value = salary_structure.custom_samples_table.custom_samples_table[0].base_salary
	# custom_samples_table = salary_structure.custom_samples_table
	# if employee.marital_status == 'Married' and employee.custom_number_of_children > 0 :
	# 	samples_table = salary_structure.custom_sample_table_married_with_child
	# elif employee.marital_status =="Married" and employee.custom_number_of_children == 0:
	# 	samples_table = salary_structure.custom_sample_table_married
	# else:
	# 	samples_table = salary_structure.custom_samples_table

		# custom_samples_table = salary_structure.custom_samples_table
	if employee.marital_status == 'Married' and employee.custom_number_of_children > 0 :
		if evaluation == "Hassan":
			samples_table = salary_structure.custom_sample_table_married_with_child_hassan
		elif evaluation == "high":
			samples_table = salary_structure.custom_sample_table_married_with_child_high
		else:
			samples_table = salary_structure.custom_sample_table_married_with_child
	elif employee.marital_status =="Married" and employee.custom_number_of_children == 0:
		if evaluation == "Hassan":
			samples_table = salary_structure.custom_sample_table_married_hassan
		elif evaluation == "high":
			samples_table = salary_structure.custom_sample_table_married_high
		else:
			samples_table = salary_structure.custom_sample_table_married
	else:
		if evaluation == "Hassan":
			samples_table = salary_structure.custom_sample_table_single_hassan
		elif evaluation == "high":
			samples_table = salary_structure.custom_sample_table_single_high
		else:		
			samples_table = salary_structure.custom_samples_table

		# custom_samples_table = salary_structure.custom_samples_table
	# samples_table = salary_structure.custom_sample_table_married_with_child_hassan
# 

	x = []
	y = []
	for v in samples_table :
		print(v.base_salary)
		x.append(v.base_salary)
		y.append(v.net_salary)
	# x.sort()
	# y.sort()
		
	# print("jjjjjjjjjj" , x)
	# print(y)
		
	# Create an interpolation function
	# interp_func = CubicSpline(y, x)
	interp_func = interpolate.interp1d(y, x, kind='linear')

	# Define a y value for which you want to find the corresponding x
	desired_y = custom_net_salary
	estimated_x = interp_func(desired_y)
	print(f"The estimated x for y={desired_y} is approximately {estimated_x}")
	return float(estimated_x)

def check_discount_percent(doc, method):
	user = frappe.session.user

	doctype = frappe.get_doc("Sales Invoice Discount Percentage")

	percent = 0

	for row in doctype.discount_percentage:
		if row.user == user:
			percent = row.discount_percent
	
	
	if doc.additional_discount_percentage > percent:
		frappe.throw(_("Additional Discount Percentage should be less or equal to " + str(percent)))


