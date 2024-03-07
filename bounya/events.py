import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
import json
from frappe.utils import (
    flt,
    getdate,
    nowdate,
)


@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
    def update_item(obj, target, source_parent):
        qty = (
            flt(flt(obj.stock_qty) - flt(obj.ordered_qty)) / target.conversion_factor
            if flt(obj.stock_qty) > flt(obj.ordered_qty)
            else 0
        )
        target.qty = qty
        target.transfer_qty = qty * obj.conversion_factor
        target.conversion_factor = obj.conversion_factor

        if (
            source_parent.material_request_type == "Material Transfer"
            or source_parent.material_request_type == "Customer Provided"
        ):
            target.t_warehouse = obj.warehouse
        else:
            target.s_warehouse = obj.warehouse

        if source_parent.material_request_type == "Customer Provided":
            target.allow_zero_valuation_rate = 1

        if source_parent.material_request_type == "Material Transfer":
            target.s_warehouse = obj.from_warehouse

    def set_missing_values(source, target):
        target.purpose = source.material_request_type
        target.from_warehouse = source.set_from_warehouse
        target.to_warehouse = source.set_warehouse

        if source.material_request_type == _("Material Issue"):
            target.custom_branch = source.custom_branch
            target.custom_department = source.custom_department
            target.custom_cost_center = source.custom_cost_center
            target.custom_project = source.custom_project

        if source.job_card:
            target.purpose = "Material Transfer for Manufacture"

        if source.material_request_type == "Customer Provided":
            target.purpose = "Material Receipt"

        target.set_transfer_qty()
        target.set_actual_qty()
        target.calculate_rate_and_amount(raise_error_if_no_rate=False)
        target.stock_entry_type = target.purpose
        target.set_job_card_data()

        if source.job_card:
            job_card_details = frappe.get_all(
                "Job Card",
                filters={"name": source.job_card},
                fields=["bom_no", "for_quantity"],
            )

            if job_card_details and job_card_details[0]:
                target.bom_no = job_card_details[0].bom_no
                target.fg_completed_qty = job_card_details[0].for_quantity
                target.from_bom = 1

    doclist = get_mapped_doc(
        "Material Request",
        source_name,
        {
            "Material Request": {
                "doctype": "Stock Entry",
                "validation": {
                    "docstatus": ["=", 1],
                    "material_request_type": [
                        "in",
                        ["Material Transfer", "Material Issue", "Customer Provided"],
                    ],
                },
            },
            "Material Request Item": {
                "doctype": "Stock Entry Detail",
                "field_map": {
                    "name": "material_request_item",
                    "parent": "material_request",
                    "uom": "stock_uom",
                    "job_card_item": "job_card_item",
                },
                "postprocess": update_item,
                "condition": lambda doc: (
                    flt(doc.ordered_qty, doc.precision("ordered_qty"))
                    < flt(doc.stock_qty, doc.precision("ordered_qty"))
                ),
            },
        },
        target_doc,
        set_missing_values,
    )

    return doclist


@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None, args=None):
    if args is None:
        args = {}
    if isinstance(args, str):
        args = json.loads(args)

    def postprocess(source, target_doc):
        if frappe.flags.args and frappe.flags.args.default_supplier:
            # items only for given default supplier
            supplier_items = []
            for d in target_doc.items:
                default_supplier = get_item_defaults(
                    d.item_code, target_doc.company
                ).get("default_supplier")
                if frappe.flags.args.default_supplier == default_supplier:
                    supplier_items.append(d)
            target_doc.items = supplier_items

        set_missing_values(source, target_doc)

    def select_item(d):
        filtered_items = args.get("filtered_children", [])
        child_filter = d.name in filtered_items if filtered_items else True

        return d.ordered_qty < d.stock_qty and child_filter

    doclist = get_mapped_doc(
        "Material Request",
        source_name,
        {
            "Material Request": {
                "doctype": "Purchase Order",
                "validation": {
                    "docstatus": ["=", 1],
                    "material_request_type": ["=", "Purchase"],
                },
            },
            "Material Request Item": {
                "doctype": "Purchase Order Item",
                "field_map": [
                    ["name", "material_request_item"],
                    ["parent", "material_request"],
                    ["uom", "stock_uom"],
                    ["uom", "uom"],
                    ["sales_order", "sales_order"],
                    ["sales_order_item", "sales_order_item"],
                ],
                "postprocess": update_item,
                "condition": select_item,
            },
        },
        target_doc,
        postprocess,
    )

    return doclist


def set_missing_values(source, target_doc):
    if target_doc.doctype == "Purchase Order" and getdate(
        target_doc.schedule_date
    ) < getdate(nowdate()):
        target_doc.schedule_date = None
    target_doc.run_method("set_missing_values")
    target_doc.run_method("calculate_taxes_and_totals")

    target_doc.custom_branch = source.custom_branch
    target_doc.custom_department = source.custom_department
    target_doc.cost_center = source.custom_cost_center
    target_doc.project = source.custom_project


def update_item(obj, target, source_parent):
    target.conversion_factor = obj.conversion_factor
    target.qty = (
        flt(flt(obj.stock_qty) - flt(obj.ordered_qty)) / target.conversion_factor
    )
    target.stock_qty = target.qty * target.conversion_factor
    if getdate(target.schedule_date) < getdate(nowdate()):
        target.schedule_date = None


def validate_rule(self):
    if not self.approving_role and not self.approving_user:
        frappe.throw(_("Please enter Approving Role or Approving User"))
    elif self.system_user and self.system_user == self.approving_user:
        frappe.throw(
            _("Approving User cannot be same as user the rule is Applicable To")
        )
    elif self.system_role and self.system_role == self.approving_role:
        frappe.throw(
            _("Approving Role cannot be same as role the rule is Applicable To")
        )
    elif self.transaction in [
        "Purchase Order",
        "Purchase Receipt",
        "Purchase Invoice",
        "Stock Entry",
    ] and self.based_on in [
        "Average Discount",
        "Customerwise Discount",
        "Itemwise Discount",
    ]:
        frappe.throw(
            _("Cannot set authorization on basis of Discount for {0}").format(
                self.transaction
            )
        )
    elif self.based_on == "Average Discount" and flt(self.value) > 100.00:
        frappe.throw(_("Discount must be less than 100"))
    elif self.based_on == "Customerwise Discount" and not self.master_name:
        frappe.throw(_("Customer required for 'Customerwise Discount'"))
    else:
        pass
