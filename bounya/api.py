import re
import frappe
from frappe import _, msgprint,throw
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt
from frappe.utils.data import money_in_words

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
		frappe.throw(msg, title=_("Error"))
		frappe.msgprint(e)
	


# this code work in employee fileds for bank branches
@frappe.whitelist()
def fetch_bank_branch_list(doctype, txt, searchfield, start, page_len, filters):

	return frappe.db.sql(
		"""
        SELECT branch_name
        FROM `tabEmployee Bank Branch`
        WHERE parent = %(bank_name)s
		and `branch_name` LIKE %(txt)s
        """.format(
			key=searchfield
		),
		{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len , "bank_name": filters.get("bank_name")},
	)

# this code work in employee fileds for office branches
@frappe.whitelist()
def fetch_branchs_office_list(doctype, txt, searchfield, start, page_len, filters):

	return frappe.db.sql(
		"""
        SELECT office_name
        FROM `tabBranches Offices`
        WHERE parent = %(branch)s
		and `office_name` LIKE %(txt)s
        """.format(
			key=searchfield
		),
		{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len , "branch": filters.get("branch")},
	)


@frappe.whitelist()
def fetch_base_from_slip(grade , marbot):
	grade = frappe.get_doc("Employee Grade", grade)
	if(cint(marbot) > 0):
		return (grade.default_base_pay + (grade.custom_dependent_value * (cint(marbot) - 1)))
	else:
		return (grade.default_base_pay )
	
@frappe.whitelist()
def update_base_from_slip(doc ,method):
	# frappe.msgprint("hi")
	if (doc.grade):
		grade = frappe.get_doc("Employee Grade", doc.grade)
		if(cint(doc.custom_dependent) > 0):
			doc.custom_net_salary = grade.default_base_pay + (grade.custom_dependent_value * (cint(doc.custom_dependent) - 1))
		else:
			doc.custom_net_salary = grade.default_base_pay 
		# doc.save()
		frappe.db.commit()

# @frappe.whitelist()
# def money_in_words(number):
#     result = money_in_words(number)

#     return _(result)


@frappe.whitelist()

def money_in_words(number, main_currency = None, fraction_currency=None):
    """
    Returns string in words with currency and fraction currency.
    """
    from frappe.utils import get_defaults, in_words, get_number_format_info
    _ = frappe._
    # delete the word 'واحد' from the number words if start with 1
    start_in_one_word = str(number).startswith("1")
    try:
        # note: `flt` returns 0 for invalid input and we don't want that
        number = float(number)
    except ValueError:
        return ""

    number = flt(number)
    if number < 0:
        return ""

    d = get_defaults()
    if not main_currency:
        main_currency = d.get("currency", "USD")
    if not fraction_currency:
        fraction_currency = frappe.db.get_value("Currency", main_currency, "fraction", cache=True) or _("Cent")

    number_format = frappe.db.get_value("Currency", main_currency, "number_format", cache=True) or \
        frappe.db.get_default("number_format") or "#,###.##"

    fraction_length = get_number_format_info(number_format)[2]

    n = "%.{0}f".format(fraction_length) % number

    numbers = n.split(".")
    main, fraction =  numbers if len(numbers) > 1 else [n, "00"]

    if len(fraction) < fraction_length:
        zeros = "0" * (fraction_length - len(fraction))
        fraction += zeros

    in_million = True
    if number_format == "#,##,###.##": in_million = False

    fraction_currency = _(fraction_currency)
    main_currency = _(main_currency)
    # 0.00
    if main == "0" and fraction in ["00", "000"]:
        out = "{0} {1}".format(main_currency, _("Zero"))
    # 0.XX
    elif main == "0":
        out = _(in_words(fraction, in_million).title()) + " " + fraction_currency
    else:
        out = _(in_words(main, in_million).title()) + " " + main_currency
        if cint(fraction):
            out = out + " " + _("and") + " " + _(in_words(fraction, in_million).title()) + " " + fraction_currency

    if start_in_one_word and out[:4] == 'واحد':
        out = out[5:]

    out = re.sub(r'(\b\w*ائة)(\w+\b)', r'\1 و \2', out)
    out = re.sub(r'(\b\w*ئتان)(\w+\b)', r'\1 و \2', out)
    # return out + " " + _("only.")
    return out 

