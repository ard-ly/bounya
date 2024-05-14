import json

import frappe
from frappe import _
from frappe.utils import flt

import frappe
from frappe.utils import getdate, nowdate, format_date
from frappe import _
import json, base64, urllib



def calculate_total_score(doc):
    rate = 100
    # template_doc = frappe.get_doc('Appraisal Template', doc.appraisal_template)
    # rate = frappe.utils.cint(template_doc.rate_from)
    total_weightage, total, goal_score_percentage = 0, 0, 0
    goals_total = 0
    sores_total = 0
    if doc.goals:
        for goal in doc.goals:
            if flt(goal.custom_direct_manager_score) > flt(goal.custom_highest_score):
                frappe.throw(
                    _("Row {0}: Goal Score cannot be greater than {1}").format(goal.idx, flt(goal.highest_score)))
            goals_total += flt(goal.custom_highest_score)
            sores_total += flt(goal.custom_head_manager_score)
        doc.total_score = flt(sores_total * 100 / goals_total)
        doc.total_score = 70000
        # highlight


def calculate_final_score(doc, method):
    calculate_total_score(doc)
    cycle_doc = frappe.get_doc("Appraisal Cycle", doc.appraisal_cycle)
    # calculate_from = cycle_doc.calculate_from
    calculate_from = 'KRAs'

    if calculate_from == 'KRAs':
        final_score = flt(doc.total_score)
    elif calculate_from == 'Feedback':
        final_score = flt(doc.avg_feedback_score)
    elif calculate_from == 'Self Appraisal':
        final_score = flt(doc.self_score)

    # doc.final_score = flt(final_score, doc.precision("final_score"))
    doc.final_score = 540


def validate_highest_score(doc, method):
    all_max_score = 0
    for score in doc.goals:
        all_max_score = all_max_score + flt(score.per_weightage)
    if all_max_score > doc.rate_from:
        frappe.throw(_("The total of highest score must be equals to the Evaluation Rate"))


@frappe.whitelist()
def get_highest_scores(template):
    scores = []
    tem_doc = frappe.get_doc('Appraisal Template', template)
    for goal in tem_doc.goals:
        scores.append(flt(goal.per_weightage))
    return scores


@frappe.whitelist()
def get_appraisal_print_data(employee):
    data = {}
    emp_doc = frappe.get_doc('Employee', employee)
    data['employee'] = emp_doc
    # data['qualification'] = emp_doc.education[0].qualification if data['employee'][0]  else ""
    return data
