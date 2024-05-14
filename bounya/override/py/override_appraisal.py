import json

import frappe
from frappe import _
from frappe.utils import flt

import frappe
from hrms.hr.doctype.appraisal.appraisal import Appraisal
from frappe.utils import getdate, nowdate, format_date
from frappe import _
import json, base64, urllib


class CustomAppraisal(Appraisal):
#     def calculate_total_score(self):
#         total_weightage, total, goal_score_percentage = 0, 0, 0

#         if self.rate_goals_manually:
#             table = _("Goals")
#             for entry in self.goals:
#                 if flt(entry.score) > 5:
#                     frappe.throw(_("Row {0}: Goal Score cannot be greater than 5").format(entry.idx))

#                 entry.score_earned = flt(entry.score) * flt(entry.per_weightage) / 100
#                 total += flt(entry.score_earned)
#                 total_weightage += flt(entry.per_weightage)

#         else:
#             table = _("KRAs")
#             for entry in self.appraisal_kra:
#                 goal_score_percentage += flt(entry.goal_score)
#                 total_weightage += flt(entry.per_weightage)

#             self.goal_score_percentage = flt(goal_score_percentage, self.precision("goal_score_percentage"))
#             # convert goal score percentage to total score out of 5
#             total = flt(goal_score_percentage) / 20

#         if total_weightage and flt(total_weightage, 2) != 100.0:
#             frappe.throw(
#                 _("Total weightage for all {0} must add up to 100. Currently, it is {1}%").format(
#                     table, total_weightage
#                 ),
#                 title=_("Incorrect Weightage Allocation"),
#             )

#         self.total_score = flt(total, self.precision("total_score"))
#         # self.total_score = flt(70)

#     def calculate_final_score(self):
#         final_score = flt(self.total_score)

#         self.final_score = flt(final_score, self.precision("final_score"))


#     def validate_highest_score(doc):
#         all_max_score = 0
#         for score in doc.goals:
#             all_max_score = all_max_score + score.custom_highest_score
#         if all_max_score > doc.rate_from:
#             frappe.throw(_("The total of highest score must be equals to the Evaluation Rate"))


# @frappe.whitelist()
# def get_highest_scores(template):
#     scores = []
#     tem_doc = frappe.get_doc('Appraisal Template', template)
#     for goal in tem_doc.goals:
#         scores.append(goal.custom_highest_score)
#     return scores


# @frappe.whitelist()
# def get_appraisal_print_data(employee):
#     data = {}
#     emp_doc = frappe.get_doc('Employee', employee)
#     data['employee'] = emp_doc
#     # data['qualification'] = emp_doc.education[0].qualification if data['employee'][0]  else ""
#     return data

    def calculate_total_score(doc):
        rate = 100
        # template_doc = frappe.get_doc('Appraisal Template', doc.appraisal_template)
        # rate = frappe.utils.cint(template_doc.rate_from)
        total_weightage, total, goal_score_percentage = 0, 0, 0
        goals_total = 0
        sores_total = 0
        if doc.goals:
            for goal in doc.goals:
                if flt(goal.custom_direct_manager_score) > flt(goal.per_weightage):
                    frappe.throw(
                        _("Row {0}: Goal Score cannot be greater than {1}").format(goal.idx, flt(goal.per_weightage)))
                goals_total += flt(goal.per_weightage)
                sores_total += flt(goal.custom_direct_manager_score)
            doc.total_score = flt(sores_total * 100 / goals_total)
            # highlight


    def calculate_final_score(doc):
        doc.calculate_total_score()
        cycle_doc = frappe.get_doc("Appraisal Cycle", doc.appraisal_cycle)
        # calculate_from = cycle_doc.calculate_from
        final_score = flt(doc.total_score)
        doc.final_score = flt(final_score, doc.precision("final_score"))

        # set the evaluation score
        performens_list = frappe.get_all('Appraisal Setting CT', filters={'parent': 'Appraisal Setting', }, fields=['appraisal_weightage' , 'evaluation' , 'performance_factor'], order_by='performance_factor')
        evaluation = ""
        performance_factor = 0.0
        for pr in performens_list:
            if final_score <= pr.appraisal_weightage:
                print(pr.evaluation)
                evaluation = pr.evaluation
                performance_factor = pr.performance_factor
                break

        doc.custom_evaluation = evaluation 
        doc.custom_performance_factor = performance_factor



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
