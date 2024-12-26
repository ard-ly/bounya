# Copyright (c) 2024, ARD Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from pymysql import MySQLError
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate, time_diff, time_diff_in_hours
from datetime import datetime

class MailImport(Document):
    @frappe.whitelist()
    def import_mail_data(self):
        directory_type = 'public'
        if '/private/' in self.attach_file:
            directory_type = 'private'

        from frappe.utils.csvutils import read_csv_content
        file_name = self.attach_file.split('/')[-1]
        file_path = frappe.get_site_path(directory_type, 'files', file_name)

        try:
            with open(file_path, "r") as infile:
                rows = read_csv_content(infile.read())
                i = 0
                for index, row in enumerate(rows):
                    if index!=0:
                        if self.mail_type=='Incoming Mail':
                            if row[0] and row[2] and row[3] and row[4] and row[5]:
                                if not frappe.db.exists("Incoming Mail", {"reference_number": row[1]}):
                                    try:
                                        doc = frappe.new_doc("Incoming Mail")
                                        doc.update({
                                            "doctype":"Incoming Mail",
                                            "incoming_message_date": convert_date_format(str(row[0])),
                                            "reference_number": row[1],
                                            "from": row[2],
                                            "to": row[3],
                                            "message_subject": row[4],
                                            "message_registration_date": convert_date_format(str(row[5])),
                                            "notes": row[6],
                                            "docstatus": 1
                                        })
                                        doc.flags.ignore_validate = True
                                        doc.flags.ignore_mandatory = True
                                        doc.save(ignore_permissions=True)
                                        frappe.db.commit()
                                    except MySQLError as e:
                                        if e.args[0] == 1292:
                                            frappe.msgprint("Error!", alert=True, indicator='red')
                                            return f"Incorrect date value: {e.args[1]}"
                                        else:
                                            frappe.msgprint("Error!", alert=True, indicator='red')
                                            return f"Error: {e.args[1]}"
                                        continue

                                    i+=1
                                    print(f"- Successfully add mail: {row[4]}")
                                    frappe.msgprint(f"- Successfully add mail: {row[4]}", alert=True, indicator='green')
                        
                        elif self.mail_type=='Outgoing Mail':
                            if row[0] and row[2] and row[3] and row[4]:
                                if not frappe.db.exists("Outgoing Mail", {"reference_number": row[1]}):
                                    try:
                                        doc = frappe.new_doc("Outgoing Mail")
                                        doc.update({
                                            "doctype":"Outgoing Mail",
                                            "message_registration_date": convert_date_format(str(row[0])),
                                            "reference_number": row[1],
                                            "from": row[2],
                                            "to": row[3],
                                            "message_subject": row[4],
                                            "notes": row[5],
                                            "docstatus": 1
                                        })
                                        doc.flags.ignore_validate = True
                                        doc.flags.ignore_mandatory = True         
                                        doc.save(ignore_permissions=True)
                                        frappe.db.commit()
                                    except MySQLError as e:
                                        if e.args[0] == 1292:
                                            frappe.msgprint("Error!", alert=True, indicator='red')
                                            return f"Incorrect date value: {e.args[1]}"
                                        else:
                                            frappe.msgprint("Error!", alert=True, indicator='red')
                                            return f"Error: {e.args[1]}"
                                        continue

                                    i+=1
                                    print(f"- Successfully add mail: {row[4]}")
                                    frappe.msgprint(f"- Successfully add mail: {row[4]}", alert=True, indicator='green')
                        
                        else:
                            return "Missing Data!" 
                print('*************')
                frappe.msgprint("Success!", alert=True, indicator='green')
                return f"Total mail added: {i}"
        except Exception as e:
            frappe.msgprint("Error!", alert=True, indicator='red')
            return f"An error occurred: {e}"
            

def convert_date_format(date_str):
    # List of possible date formats that the user might use
    date_formats = [
        "%d-%m-%Y",  # DD-MM-YYYY (e.g., 10-02-2005)
        "%d/%m/%Y",  # DD/MM/YYYY (e.g., 10/02/2005)
        "%Y-%m-%d",  # YYYY-MM-DD (e.g., 2005-02-10)
        "%Y/%m/%d",  # YYYY/MM/DD (e.g., 2005/02/10)
        "%d.%m.%Y",  # DD.MM.YYYY (e.g., 10.02.2005)
        "%m-%d-%Y",  # MM-DD-YYYY (e.g., 02-10-2005)
        "%m/%d/%Y"   # MM/DD/YYYY (e.g., 02/10/2005)
    ]
    
    for date_format in date_formats:
        try:
            # Attempt to parse the date string with each format
            date_obj = datetime.strptime(date_str, date_format)
            # Return the date in ERPNext format YYYY-MM-DD
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            # Continue to the next format if parsing fails
            continue

    # If no format matched, log the error and return None
    frappe.msgprint(f"Error in date format conversion: Invalid date format '{date_str}'", alert=True, indicator='red')
    return None

