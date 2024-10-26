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


@frappe.whitelist()
def create_contract(document, customer_name=None):
    doc = frappe.new_doc("Contract")
    doc.document_type = "Quotation"
    doc.document_name = document
    doc.party_type = 'Customer'
    doc.party_name = customer_name if customer_name else ""
    
    doc.flags.ignore_validate = True
    doc.flags.ignore_mandatory = True
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    return doc.name


# @frappe.whitelist()
# def order_earnings(salary_detail_earnings):
#     try:
#         earnings=[ "أساسي", "سكن", "مواصلات", "علاوة قيادية", "علاوة اشرافية", "أداء", "علاوة خطر", "بدل كروت", "بدل وقود", "بدل اعاشة", "علاوة", "مكافاة خاضعة", "مكافاة غير خاضعة", "إضافي", "مبيت", "رد غياب", "بدل إجازة", "فرق خطر", "فرق اعاشة", "فرق أساسي", "فرق سكن", "فرق قيادية", "فرق اشرافية", "فرق أداء", "فرق كروت", "فرق وقود", "رعاية صحية", "الإجمالي"]
#         deductions=["حصة المضمون",	"استقطاع الصندوق" ,"خصم مركوب", "صندوق التضامن","سلفة الشركة", "خصم غياب","الجهاد"	,"سلفة الصندوق"	,"خصم نقدي","الدخل"	,"التزام مالي"	, "خصم فرق مرتب","خصم نفقة"	,"قرض"	,"خصومات اخرى","قسط تمليك"	,"سلفة رعاية" , "حصة جهة العمل"	,"الدمغة" ,"الخصميات"]
        
#         output = ''
#         return output
    
#     except ValueError:
#         throw(_("Can not order earnings and deductions."))