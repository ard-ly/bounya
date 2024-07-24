# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _, msgprint, throw
from frappe.utils import today, date_diff
from datetime import date, timedelta


class MonthlyPromotion(Document):

    def validate(self):
        self.send_promotion_notification()

    def on_submit(self):
        self.create_promotion()

    def on_cancel(self):
        self.cancel_promotion()

    def send_promotion_notification(self):
        self.status = 'Open'
        # send notification to the HR:
        users = frappe.db.sql(
            f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE (role = 'HR User' or role ='HR Manager') AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
        for user in users:
            new_doc = frappe.new_doc("Notification Log")
            new_doc.from_user = frappe.session.user
            new_doc.for_user = user.parent
            new_doc.type = "Share"
            new_doc.document_type = "Monthly Promotion"
            new_doc.document_name = self.name
            new_doc.subject = f"""New Monthly Promotion Created: {self.name}"""
            new_doc.email_content = "empty@empty.com"
            new_doc.insert(ignore_permissions=True)

    def create_promotion(self):
        self.status = 'Approved'
        if len(self.employee_table) > 0:
            for e in self.employee_table:
                try:
                    prom = frappe.new_doc("Employee Promotion")
                    prom.employee = e.employee
                    prom.promotion_date = e.promotion_date
                    prom.custom_monthly_promotion = self.name
                    prom.custom_created_by_monthly_promotion = 1
                    if e.new_grade != 0:
                        prom.append(
                            "promotion_details",
                            {
                                "property": 'Grade',
                                "current": e.current_grade,
                                "new": e.new_grade,
                            },
                        )
                    if e.new_dependent != 0:
                        prom.append(
                            "promotion_details",
                            {
                                "property": 'Dependent',
                                "current": e.current_dependent,
                                "new": e.new_dependent,
                            },
                        )
                    prom.save()
                    frappe.db.set_value("Monthly Promotion Table", e.name,
                                        "employee_promotion", prom.name)
                    prom.submit()
                    frappe.db.commit()

                except Exception as e:
                    frappe.log_error("Error while creating Employee Promotion")
                    return
        else:
            throw(_("Employees table canot be empty."))

    def cancel_promotion(self):
        self.status = 'Rejected'
        for e in self.employee_table:
            try:
                if e.employee_promotion:
                    prom = frappe.get_doc(
                        "Employee Promotion", e.employee_promotion)
                    prom.cancel()
                    frappe.db.commit()

            except Exception as e:
                frappe.log_error("Error while cencelling Employee Promotion")
                return

    @frappe.whitelist()
    def get_employees(self):
        employees = {}
        employees = frappe.db.sql(
            f""" SELECT *  FROM `tabEmployee` WHERE status = 'Active' AND custom_contract_type = 'Local contract' """, as_dict=1)

        if len(employees) > 0:
            for emp in employees:
                if emp.designation:
                    designation_doc = frappe.get_doc('Designation', emp.designation)
                    if emp.grade:
                        try:
                            if emp.custom_last_promotion_date:
                                
                                if designation_doc.custom_grade_promotion_year:
                                    # check the comparison.
                                    # print(date_diff(date.today(), emp.custom_last_promotion_date) > (designation_doc.custom_grade_promotion_year * 340))
                                    if date_diff(date.today(), emp.custom_last_promotion_date) > (designation_doc.custom_grade_promotion_year * 340):
                                        if designation_doc.custom_designation_grade:
                                            for row in designation_doc.custom_designation_grade:
                                                if row.from_grade == emp.grade:
                                                    self.append(
														"employee_table",
														{
															"employee": emp.name,
															"full_name": emp.full_name,
															"branch": emp.branch,
															"designation": emp.designation,
															"current_grade": emp.grade,
															"new_grade": row.to_grade,
															"current_dependent": emp.custom_dependent,
															"new_dependent": emp.custom_dependent+1, },)

                                    elif designation_doc.custom_dependent_promotion_year:
                                        if date_diff(date.today(), emp.custom_last_promotion_date) > (designation_doc.custom_dependent_promotion_year * 340):
                                            self.append(
                                                "employee_table",
                                                {
                                                    "employee": emp.name,
                                                    "full_name": emp.full_name,
                                                    "branch": emp.branch,
                                                    "designation": emp.designation,
                                                    "current_grade": emp.grade,
                                                    "current_dependent": emp.custom_dependent,
                                                    "new_dependent": emp.custom_dependent+1,
                                                },)

                            elif emp.date_of_joining:
                                if designation_doc.custom_grade_promotion_year:
                                    if date_diff(date.today(), emp.date_of_joining) > (designation_doc.custom_grade_promotion_year * 340):
                                        if designation_doc.custom_designation_grade:
                                            for row in designation_doc.custom_designation_grade:
                                                if row.from_grade == emp.grade:
                                                    self.append(
														"employee_table",
														{
															"employee": emp.name,
															"full_name": emp.full_name,
															"branch": emp.branch,
															"designation": emp.designation,
															"current_grade": emp.grade,
															"new_grade": row.to_grade,
															"current_dependent": emp.custom_dependent,
															"new_dependent": emp.custom_dependent+1, },)
                                
                                    elif designation_doc.custom_dependent_promotion_year:
                                        if date_diff(date.today(), emp.date_of_joining) > (designation_doc.custom_dependent_promotion_year * 340):
                                            self.append(
                                                "employee_table",
                                                {
                                                    "employee": emp.name,
                                                    "full_name": emp.full_name,
                                                    "branch": emp.branch,
                                                    "designation": emp.designation,
                                                    "current_grade": emp.grade,
                                                    "current_dependent": emp.custom_dependent,
                                                    "new_dependent": emp.custom_dependent+1,
                                                },)
                                
                        except Exception as emp:
                            frappe.log_error("Error while Getting Employees")
                    
                    # elif emp.custom_dependent

        elif len(employees) == 0:
            msgprint(
                _("There is no Active employess with contract type = Local contract ."))

        return (str(employees))