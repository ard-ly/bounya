from frappe import _

def get_data():
	return {
		"fieldname": "custom_monthly_variables",
		"non_standard_fieldnames": {"Auto Repeat": "reference_document"},
		"internal_links": {
			# "Additional Salary": ["items", ""],
		},
		"transactions": [
			{"label": _("Related"), "items": ["Additional Salary"]},
			
		],
	}
