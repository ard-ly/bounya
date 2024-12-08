app_name = "bounya"
app_title = "Albounya"
app_publisher = "ARD Company"
app_description = "Albounya"
app_email = "Hadeel.milad@ard.ly"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bounya/css/bounya.css"
# app_include_js = "/assets/bounya/js/bounya.js"
app_include_js = [
    "/assets/bounya/js/map_defaults.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/bounya/css/bounya.css"
# web_include_js = "/assets/bounya/js/bounya.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bounya/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

doctype_js = {
    "Salary Structure": "public/js/salary_structure.js",
    "Salary Structure Assignment": "public/js/salary_structure_assignment.js",
    "Employee": "public/js/employee.js",
    "Material Request": "public/js/material_request.js",
    "Additional Salary": "public/js/additional-salary.js",
    "Appraisal": "public/js/appraisal.js",
    "Appraisal Template": "override/js/appraisal_template.js",
    "Salary Slip": "public/js/salary_slip.js",
    "Payroll Entry": "public/js/payroll_entry.js",
    "Loan Application": "public/js/loan_application.js",
    "Contract":"public/js/contract.js",
    "Purchase Order":"public/js/purchase_order.js",
    "Sales Order":"public/js/sales_order.js",
    "Quotation" : "public/js/quotation.js",
    "Lead" : "public/js/lead.js",
    "Opportunity":"public/js/opportunity.js",
}
doctype_list_js = {
    "Salary Slip": "public/js/salary_slip.js",
    "Additional Salary": "public/js/additional-salary.js",
    "Salary Structure Assignment": "public/js/salary_structure_assignment.js",
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# standard_queries = {"Additional Salary": "bounya.queries.designation_query"}


# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "bounya.utils.jinja_methods",
# 	"filters": "bounya.utils.jinja_filters"
# }

jinja = {
    "methods": "bounya.utils.grad_in_words",
}


# jenv = {
#     "methods": {
#         "calculate_total": "custom_app.utils.calculate_total"
#     }
# }

jenv = {
    "methods": {
        "grad_in_words": "bounya.utils.grad_in_words",
        # "order_earnings":"bounya.utils.order_earnings",
        "grad_in_words": "bounya.utils.grad_in_words",
        # "order_earnings":"bounya.utils.order_earnings",
    }
}


# Installation
# ------------

# before_install = "bounya.install.before_install"
# after_install = "bounya.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bounya.uninstall.before_uninstall"
# after_uninstall = "bounya.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bounya.utils.before_app_install"
# after_app_install = "bounya.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bounya.utils.before_app_uninstall"
# after_app_uninstall = "bounya.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bounya.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "*":"bounya.permission_query_condition_creator.get_permission_query_conditions"
}

# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Appraisal": "bounya.override.py.override_appraisal.CustomAppraisal",
    "Salary Slip": "bounya.override.py.salary_slip.CustomSalarySlip",
    "Payroll Entry": "bounya.override.py.payroll_entry.CustomPayrollEntry",
}

# Document Events
# ---------------
# Hook on document methods and events


doc_events = {
    "Material Request": {
        "validate": "bounya.api.check_custom_has_assets",
    },
    "Employee Promotion": {
        "on_submit": "bounya.api.create_external_work_history",
        "on_cancel": "bounya.api.cancel_external_work_history",
    },
    "Additional Salary": {
        "validate": "bounya.api.get_employee_salary_slip",
        "on_submit": "bounya.api.overwrite_salary_slip",
        "on_cancel": "bounya.api.cancel_salary_slip_overwrite",
    },
    "Salary Slip": {
        "validate": "bounya.api.check_for_employee_external_advance",
        "on_submit": "bounya.api.update_external_advance_on_submit",
        "on_cancel": "bounya.api.update_external_advance_on_cancel",
    },
    # "Salary Component": {
    #     "validate": "bounya.api.update_component_order",
    # },
    "Supplier": {
        "on_update": "bounya.api.set_custom_supplier_group_sequence_field",
    },
    "Asset":{
        "on_submit": "bounya.api.add_building_accessories",
        "on_cancel": "bounya.api.cancel_building_accessories",
    },
    "Asset Movement":{
        "on_submit": "bounya.api.update_cost_center_on_submit",
        "on_cancel": "bounya.api.update_cost_center_on_cancel",
    },
    "Sales Order":{
        "on_submit": "bounya.api.update_realty_available_area_on_submit",
        "on_cancel": "bounya.api.update_realty_available_area_on_cancel",
    },
}

# doc_events = {
# 	"Salary Structure Assignment": {
# 		"on_update": "bounya.api.update_base_from_slip",
# 	}
# }


# Scheduled Tasks
# ---------------

scheduler_events = {

	"monthly": [
		"bounya.tasks.calculate_exp_yrears_in_employee",
        "bounya.tasks.calculate_tower_age"
	],
}


# scheduler_events = {
# 	"all": [
# 		"bounya.tasks.all"
# 	],
# 	"daily": [
# 		"bounya.tasks.daily"
# 	],
# 	"hourly": [
# 		"bounya.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bounya.tasks.weekly"
# 	],
# 	"monthly": [
# 		"bounya.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "bounya.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "erpnext.stock.doctype.material_request.material_request.make_stock_entry": "bounya.events.make_stock_entry",
    "erpnext.stock.doctype.material_request.material_request.make_purchase_order": "bounya.events.make_purchase_order",
    # "hrms.payroll.doctype.payroll_entry.payroll_entry.make_payment_entry" :"bounya.override.py.payroll_entry.make_payment_entry",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bounya.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

ignore_links_on_delete = ["Salary SLip", "Additional Salary"]
ignore_links_on_delete = ["Additional Salary", "Salary SLip"]
ignore_links_on_delete = ["Department", "Salary Slip", "Additional Salary" , "Employee" , "Monthly Variables" , "Salary Structure Assignment" , "Payroll Entry" , "Employee External Loans"]
# Request Events
# ----------------
# before_request = ["bounya.utils.before_request"]
# after_request = ["bounya.utils.after_request"]

# Job Events
# ----------
# before_job = ["bounya.utils.before_job"]
# after_job = ["bounya.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bounya.auth.validate"
# ]


# fixtures = [
#     {"dt": "Salary Component"},
#     {"dt": "Salary Structure", "filters": [
#         [
#             "name", "in", [
#                 "Salary Structure 2024"
#             ]
#         ]
#     ]}
# ]
fixtures = [
        {"dt": "DocType Layout", "filters": [["name", "in", ["Employee"]]]},
        {"dt": "Translation"},
    ]

#     {"dt": "Custom Field", "filters": [["module", "in", ["Albounya"]]]},
#     {"dt": "DocType Layout", "filters": [["name", "in", ["Employee"]]]},
#     {"dt": "Translation"},
#     # {"dt": "Kanban Board"},
#     {"dt": "Custom Field",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 [
#                     "Payroll Settings-salary_component_settings",
#                     "Leave Application-custom_leave_application_group",
#                 ],
#             ]
#         ],
#     },
#     {"dt": "Custom Field"},
#     {"dt": "Property Setter"},
#     {"dt": "Client Script"},
#     {"dt": "Letter Head",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 ["bounya","Contract LH"],
#             ]
#         ],
#     },
#     {"dt": "Equipment Name",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 ["Sector"],
#             ]
#         ],
#     },
#     # {"dt": "Equipment Name",
#     #     "filters": [
#     #         [
#     #             "name",
#     #             "in",
#     #             ["Services"],
#     #         ]
#     #     ],
#     # },
#     {"dt": "Workflow",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 [
#                     "MR Complete WF",
#                     "Monthly Promotion",
#                     "Equipment Installation Form",
#                     "Realty Rent Form",
#                 ],
#             ]
#         ],
#     },
#     {"dt": "Role",
#         "filters": [
#             [
#                 "name",
#                 "in",
#                 [   
#                     "Contracts Unit Employee",
#                     "Tower Management",
#                     "Buildings Management",
#                     "Commercial Management",
#                     "General Management",
#                     "Realty Details Manager",
#                     "Technical Management",
                    
#                 ],
#             ]
#         ],
#     },    

# ]
