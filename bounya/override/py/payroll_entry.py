

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
					sc.do_not_include_in_total,
				)

				.where(
					(ssd.parentfield == component_type)
					& (ss.name.isin(tuple([d.name for d in salary_slips])))
					& (sc.statistical_component == 0)
					& (sc.do_not_include_in_total == 0)
				)
			).run(as_dict=True)

			return salary_components

	def get_sal_slip_list(self, ss_status, as_dict=False):
		"""
		Returns list of salary slips based on selected criteria
		"""
		print("KKKKKKKKKKKKKKKKKKKKKKKKK \n kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
		ss = frappe.qb.DocType("Salary Slip")
		ss_list = (
			frappe.qb.from_(ss)
			.select(ss.name, ss.salary_structure)
			.where(
				(ss.docstatus == ss_status)
				& (ss.payroll_entry == self.name)
				& ((ss.journal_entry.isnull()) | (ss.journal_entry == ""))
				& (Coalesce(ss.salary_slip_based_on_timesheet, 0) == self.salary_slip_based_on_timesheet)
			)
		).run(as_dict=as_dict)

		return ss_list

	@frappe.whitelist()
	def make_payment_entry(self):
		self.check_permission("write")
		self.employee_based_payroll_payable_entries = {}
		process_payroll_accounting_entry_based_on_employee = frappe.db.get_single_value(
			"Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
		)

		salary_slip_name_list = frappe.db.sql(
			""" select t1.name from `tabSalary Slip` t1
			where t1.docstatus = 1 and start_date >= %s and end_date <= %s and t1.payroll_entry = %s
			""",
			(self.start_date, self.end_date, self.name),
			as_list=True,
		)

		if salary_slip_name_list and len(salary_slip_name_list) > 0:
			salary_slip_total = 0
			for salary_slip_name in salary_slip_name_list:
				salary_slip = frappe.get_doc("Salary Slip", salary_slip_name[0])

				for sal_detail in salary_slip.earnings:
					(
						is_flexible_benefit,
						only_tax_impact,
						creat_separate_je,
						statistical_component,
					) = frappe.db.get_value(
						"Salary Component",
						sal_detail.salary_component,
						[
							"is_flexible_benefit",
							"only_tax_impact",
							"create_separate_payment_entry_against_benefit_claim",
							"statistical_component",
						],
					)
					if only_tax_impact != 1 and statistical_component != 1:
						if is_flexible_benefit == 1 and creat_separate_je == 1:
							self.create_journal_entry(sal_detail.amount, sal_detail.salary_component)
						else:
							if process_payroll_accounting_entry_based_on_employee:
								self.set_employee_based_payroll_payable_entries(
									"earnings",
									salary_slip.employee,
									sal_detail.amount,
									salary_slip.salary_structure,
								)
							salary_slip_total += sal_detail.amount

				for sal_detail in salary_slip.deductions:
					(statistical_component,
					do_not_include_in_total )= frappe.db.get_value(
						"Salary Component", sal_detail.salary_component, ["statistical_component" , "do_not_include_in_total"],
					)
					if statistical_component != 1 and do_not_include_in_total != 1:
						if process_payroll_accounting_entry_based_on_employee:
							self.set_employee_based_payroll_payable_entries(
								"deductions",
								salary_slip.employee,
								sal_detail.amount,
								salary_slip.salary_structure,
							)

						salary_slip_total -= sal_detail.amount



			if salary_slip_total > 0:
				self.create_journal_entry(salary_slip_total, "salary")

