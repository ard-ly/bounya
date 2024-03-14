__version__ = "0.0.1"


from erpnext.setup.doctype.authorization_rule.authorization_rule import (
    AuthorizationRule,
)
from bounya.events import validate_rule

AuthorizationRule.validate_rule = validate_rule
