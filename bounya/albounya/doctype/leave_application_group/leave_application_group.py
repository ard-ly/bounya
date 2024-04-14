# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint,throw
from datetime import datetime
from frappe.utils import date_diff, month_diff, add_months
from frappe.model.document import Document

class LeaveApplicationGroup(Document):
	def validate(self):
		self.check_date()
		self.validate_employees()
	
	def on_submit(self):
		self.create_leave_apps()
	
	def on_cancel(self):
		self.cancel_leave_apps()


	@frappe.whitelist()
	def get_employees(self):
		employees={}
		if self.department and self.branch:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE department = '{self.department}' And branch = '{self.branch}' And status = 'Active' """,as_dict=1,)
			
		elif self.department:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE department = '{self.department}' And status = 'Active' """,as_dict=1,)
		
		elif self.branch:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE branch = '{self.branch}' And status = 'Active' """,as_dict=1,)
		
		else:
			employees =  frappe.db.sql(f""" SELECT *  FROM `tabEmployee` WHERE status = 'Active'""",as_dict=1,)

		if len(employees) > 0:
			self.save()
			for e in employees:
				new_settings = frappe.new_doc("Leave Application Group Settings")
				new_settings.employee = e.name
				new_settings.parent = self.name
				new_settings.parentfield = 'employees_table'
				new_settings.parenttype = 'Leave Application Group'
				new_settings.insert(ignore_permissions=True)

			la_settings =  frappe.db.sql(f""" SELECT *  FROM `tabLeave Application Group Settings` where parent = '{self.name}' """,as_dict=1,)
			self.total_number_of_employees = len(la_settings)

		elif len(employees) == 0:
			msgprint(_("There is no employess in this branch and this department"))

		

		return str(employees)

	def check_date(self):
		if self.to_date and self.from_date:
			if date_diff(self.to_date,self.from_date) < 0:
				throw(_("To Date must be after From Date."))
			else:
				self.total_leave_days = date_diff(self.to_date,self.from_date)+1


	def validate_employees(self):
		pass

	def create_leave_apps(self):
		if len(self.employees_table) > 0:
			for row in self.employees_table:
				try:
					leave = frappe.new_doc("Leave Application")
					leave.employee = row.employee
					leave.employee_name = row.employee_name
					leave.leave_type = self.leave_type
					leave.company = self.company
					leave.department = self.department
					leave.from_date = self.from_date
					leave.to_date = self.to_date
					leave.half_day = self.half_day
					leave.status = "Approved"
					leave.custom_leave_application_group = self.name
					leave.save()

					# add comment to the Leave Application.
					TE = f"<a href='/app/eave-application-group/{self.name}' style='color: var(--text-on-blue)'>{self.name}</a>"
					leave.add_comment("Comment",text=""" This Leave Application was created by {TE}.""".format(TE = TE), )
					
					leave.submit()
					frappe.db.commit()

				except Exception as e:
					frappe.log_error("Error while creating Leave Application for", str(e.employee))
					return

		elif len(self.employees_table) == 0:
			throw(_('Employees Table cannot be empty.'))

	def cancel_leave_apps(self):
		pass
		# 	leave_apps = frappe.db.sql(f""" SELECT *  FROM `tabLeave Application` where custom_leave_application_group = '{self.name}' """,as_dict=1,)

		# 	if len(leave_apps) > 0:
		# 		for a in leave_apps:
		# 			# a.cancel()
		# 			frappe.db.set_value("Leave Application", a.name, "docstatus", 2)
		# 			frappe.db.commit()
		# 			msgprint("doneeeeee")
			


	
