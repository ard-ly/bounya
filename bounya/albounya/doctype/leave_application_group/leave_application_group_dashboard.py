from frappe import _

def get_data():
	return {
		"fieldname": "custom_leave_application_group",
		"non_standard_fieldnames": {"Auto Repeat": "reference_document"},
		"transactions": [
			{"items": ["Leave Application"]},
			
		],
	}
