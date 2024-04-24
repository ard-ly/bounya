import frappe
from frappe import _, msgprint,throw
from frappe.model.document import Document
from frappe.utils import money_in_words


@frappe.whitelist()
def grad_in_words(value):
    try:
        in_word = frappe.utils.money_in_words(value ," ").replace("only." ,  " ") .replace("فقط." ,  " ")
        output = in_word.replace("واحد","الأولى").replace("اثنان" ,"الثانية").replace("ثلاثة" ,  "الثالثة").replace("أربعة" ,  "الرابعة").replace("خمسة" ,  "الخامسة").replace("ستة" ,  "السادسة").replace("سبعة" ,  "السابعة").replace("ثمانية" ,  "الثامنة").replace("تسعة" ,  "التاسعة").replace("عشرة" ,  "العاشرة").replace("أحد" ,  "الإحدى").replace("اثنا" ,  "الثانية")
        return output
    
    except ValueError:
        throw(_("value must be a number."))