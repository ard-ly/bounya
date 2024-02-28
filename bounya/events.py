import frappe
from frappe.utils import flt
from frappe.model.mapper import get_mapped_doc
from frappe import _


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

        if source.material_request_type == _('Material Issue'):
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
                "Job Card", filters={"name": source.job_card}, fields=["bom_no", "for_quantity"]
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
                    "material_request_type": ["in", ["Material Transfer", "Material Issue", "Customer Provided"]],
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