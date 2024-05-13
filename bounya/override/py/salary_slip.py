

import frappe
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe.utils import getdate, nowdate, format_date
from frappe import _
from frappe.query_builder import Order

import json, base64, urllib

class CustomSalarySlip(SalarySlip):
    def check_sal_struct(self, joining_date, relieving_date):
        ss = frappe.qb.DocType("Salary Structure")
        ssa = frappe.qb.DocType("Salary Structure Assignment")

        query = (
            frappe.qb.from_(ssa)
            .join(ss)
            .on(ssa.salary_structure == ss.name )
            .select(ssa.salary_structure , ssa.custom_performance_factor , ssa.custom_evaluation)
            .where(
                (ssa.docstatus == 1)
                & (ss.docstatus == 1)
                & (ss.is_active == "Yes")
                & (ssa.employee == self.employee)
                & (
                    (ssa.from_date <= self.start_date)
                    | (ssa.from_date <= self.end_date)
                    | (ssa.from_date <= joining_date)
                )
            )
            .orderby(ssa.from_date, order=Order.desc)
            .limit(1)
        )

        if not self.salary_slip_based_on_timesheet and self.payroll_frequency:
            query = query.where(ss.payroll_frequency == self.payroll_frequency)

        st_name = query.run()

        if st_name:
            self.salary_structure = st_name[0][0]
            self.custom_performance_factor = st_name[0][1]
            self.custom_evaluation = st_name[0][2]
            print (self.custom_evaluation)
            return self.salary_structure

        else:
            self.salary_structure = None
            frappe.msgprint(
                _("No active or default Salary Structure found for employee {0} for the given dates").format(
                    self.employee
                ),
                title=_("Salary Structure Missing"),
            )
                    

    # @frappe.whitelist()
    # def check_sal_struct(self, joining_date, relieving_date):
    #     ss = frappe.qb.DocType("Salary Structure")
    #     ssa = frappe.qb.DocType("Salary Structure Assignment")

    #     query = (
    #         frappe.qb.from_(ssa)
    #         .join(ss)
    #         .on(ssa.salary_structure == ss.name)
    #         .select(ssa.salary_structure , ssa.custom_performance_factor , ssa.custom_evaluation)
    #         .where(
    #             (ssa.docstatus == 1)
    #             & (ss.docstatus == 1)
    #             & (ss.is_active == "Yes")
    #             & (ssa.employee == self.employee)
    #             & (
    #                 (ssa.from_date <= self.start_date)
    #                 | (ssa.from_date <= self.end_date)
    #                 | (ssa.from_date <= joining_date)
    #             )
    #         )
    #         .orderby(ssa.from_date, order=Order.desc)
    #         .limit(1)
    #     )

    #     if not self.salary_slip_based_on_timesheet and self.payroll_frequency:
    #         query = query.where(ss.payroll_frequency == self.payroll_frequency)

    #     st_name = query.run()

    #     if st_name:
    #         self.custom_performance_factor = st_name[0][1]
    #         self.custom_evaluation = st_name[0][2]
    #         print (self.custom_evaluation)
    #         # return self.salary_structure

    #     else:
    #         self.salary_structure = None
