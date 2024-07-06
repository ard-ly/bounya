

import json

from dateutil.relativedelta import relativedelta

import frappe
from frappe import _
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.model.document import Document
from frappe.query_builder.functions import Coalesce, Count
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	get_link_to_form,
	getdate,
)

import erpnext
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from erpnext.accounts.utils import get_fiscal_year
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry


class CustomPayrollEntry(PayrollEntry):

	def get_salary_components(self, component_type):
		frappe.msgprint("Edit Hadeel")
		salary_slips = self.get_sal_slip_list(ss_status=1, as_dict=True)

		if salary_slips:
			ss = frappe.qb.DocType("Salary Slip")
			sc = frappe.qb.DocType("Salary Component")
			ssd = frappe.qb.DocType("Salary Detail")
			salary_components = (
				frappe.qb.from_(ss)
				.join(ssd)
				.on(ss.name == ssd.parent)
				.join(sc)
				.on(ssd.salary_component == sc.name)
                .select(
					ssd.salary_component,
					ssd.amount,
					ssd.parentfield,
					ssd.additional_salary,
					ss.salary_structure,
					ss.employee,
					sc.statistical_component,
				)

				.where(
					(ssd.parentfield == component_type)
					& (ss.name.isin(tuple([d.name for d in salary_slips])))
					& (sc.statistical_component == 0)
				)
			).run(as_dict=True)

			return salary_components
		

# component_type= "deductions"



	# def get_salary_components(self, component_type):
	# 	frappe.msgpritn("Edit Hadeel")
	# 	salary_slips = self.get_sal_slip_list(ss_status=1, as_dict=True)

	# 	if salary_slips:
	# 		ss = frappe.qb.DocType("Salary Slip")
	# 		sc = frappe.qb.DocType("Salary Component")
	# 		ssd = frappe.qb.DocType("Salary Detail")
	# 		salary_components = (
	# 			frappe.qb.from_(ss)
	# 			.join(ssd)
	# 			.on(ss.name == ssd.parent)
	# 			.select(
	# 				ssd.salary_component,
	# 				ssd.amount,
	# 				ssd.parentfield,
	# 				ssd.additional_salary,
	# 				ss.salary_structure,
	# 				ss.employee,
	# 			)
	# 			.join(sc)
	# 			.on(ssd.salary_component, sc.name)
	# 			.where(
	# 				(ssd.parentfield == component_type)
	# 				& (ss.name.isin(tuple([d.name for d in salary_slips])))
	# 			)
	# 		).run(as_dict=True)

	# 		return salary_components