# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _, msgprint,throw
from frappe.utils import today
from datetime import date

class Towers(Document):
	def validate(self):
		self.validate_date_of_construction()
		self.send_notification_to_Tower_management()

	
	def validate_date_of_construction(self):
		if self.date_of_construction:
			if self.date_of_construction >= today():
				throw(_("Date of construction must be before today date."))
			else:
				
				months=frappe.utils.month_diff(frappe.utils.nowdate(),self.date_of_construction)
				self.age_of_tower =  int(months)
	
	def send_notification_to_Tower_management(self):
		if self. docstatus == 0:
			users = frappe.db.sql(
				f""" SELECT DISTINCT parent FROM `tabHas Role` WHERE role = 'Tower Management' AND parenttype = 'User' AND parent != 'Administrator' """, as_dict=True)
			for user in users:
				new_doc = frappe.new_doc("Notification Log")
				new_doc.from_user = frappe.session.user
				new_doc.for_user = user.parent
				new_doc.type = "Share"
				new_doc.document_type = "Towers"
				new_doc.document_name = self.name
				new_doc.subject = f"""New Tower Created: {self.name}"""
				new_doc.email_content = "empty@empty.com"
				new_doc.insert(ignore_permissions=True)

				# mesg = "<p> New Tower Doctype Created,<br> name:"+self.tower_name+"<br>Serial Number:"+self.serial_number+"<br> branch:"+self.branch+ "<br> Office: "+self.office+ "<br> Type:"+ self.tower_type+ "</p>"
				# frappe.sendmail(
				# 	recipients=user,
				# 	subject="Tower " + self.name,
				# 	message= mesg,
				# 	now=1,
				# 	retry=3
				# )
				# frappe.db.commit()

