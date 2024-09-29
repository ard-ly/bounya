

import frappe
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe.utils import getdate, nowdate, format_date
from frappe import _
from frappe.query_builder import Order
from erpnext.loan_management.doctype.loan_repayment.loan_repayment import (
	calculate_amounts,
	create_repayment_entry,
)
import json, base64, urllib

class CustomSalarySlip(SalarySlip):
    def check_sal_struct(self, joining_date, relieving_date):
        ss = frappe.qb.DocType("Salary Structure")
        ssa = frappe.qb.DocType("Salary Structure Assignment")

        query = (
            frappe.qb.from_(ssa)
            .join(ss)
            .on(ssa.salary_structure == ss.name )
            .select(ssa.salary_structure , ssa.custom_performance_factor_ , ssa.custom_evaluation)
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
# overrid function to fetch loan type
    def set_loan_repayment(self):
        self.total_loan_repayment = 0
        self.total_interest_amount = 0
        self.total_principal_amount = 0

        if not self.get("loans"):
            for loan in self.get_loan_details():
                amount = 0
                if frappe.get_all("Loan Interest Accrual" , filters={"loan" : loan.name  ,"paid_principal_amount" :  0}, order_by="posting_date DESC", limit=1):
                    latest_Interest = frappe.get_all("Loan Interest Accrual" , filters={"loan" : loan.name  ,"paid_principal_amount" :  0}, order_by="posting_date DESC", limit=1)
                    amount=frappe.get_doc("Loan Interest Accrual" ,latest_Interest).payable_principal_amount
                else:
                    amount=frappe.get_doc("Loan" ,loan.name ).monthly_repayment_amount
                amounts = calculate_amounts(loan.name, self.start_date, "Regular Payment")

                if amounts["interest_amount"] or amounts["payable_principal_amount"]:
                    self.append(
                        "loans",
                        {
                            "loan": loan.name,
                            "total_payment": amount,
                            "interest_amount": amounts["interest_amount"],
                            "principal_amount": amount,
                            "loan_account": loan.loan_account,
                            "loan_type": loan.loan_type,
                            "interest_income_account": loan.interest_income_account,
                        },
                    )

        for payment in self.get("loans"):
            amounts = calculate_amounts(payment.loan, self.start_date, "Regular Payment")
            total_amount = amounts["interest_amount"] + amounts["payable_principal_amount"]
            if payment.total_payment > total_amount:
                frappe.throw(
                    _(
                        """Row {0}: Paid amount {1} is greater than pending accrued amount {2} against loan {3}"""
                    ).format(
                        payment.idx,
                        frappe.bold(payment.total_payment),
                        frappe.bold(total_amount),
                        frappe.bold(payment.loan),
                    )
                )

            self.total_interest_amount += payment.interest_amount
            self.total_principal_amount += payment.principal_amount

            self.total_loan_repayment += payment.total_payment

        
    def pull_emp_details(self):
        emp = frappe.db.get_value(
            "Employee", self.employee, ["custom_bank_name", "bank_ac_no", "salary_mode" ,"grade" , "custom_grade_of_assignment"], as_dict=1
        )
        if emp:
            self.mode_of_payment = emp.salary_mode
            self.bank_name = emp.custom_bank_name
            self.bank_account_no = emp.bank_ac_no
            self.custom_grade =emp.custom_grade_of_assignment or emp.grade

    # def set_status(self, status=None):
    #     """Get and update status"""
    #     if not status:
    #         status = self.get_status()
    #     print("55555555555")

    #     frappe.db.set_value("Salary Slip" , self.name , "docstatus" , 1 )


    def validate(self):
        pass