import frappe
from frappe import _
from frappe.utils import flt

@frappe.whitelist(allow_guest=True)
def qb_webhook():
    data = frappe.local.form_dict
    sku = data.get("sku")
    store_id = data.get("store_id")
    sold_qty = flt(data.get("qty_sold"))

    item = frappe.db.get_value("Item", {"qb_sku": sku}, "name")
    warehouse = frappe.db.get_value("Warehouse", {"qb_store_id": store_id}, "name")

    if not (item and warehouse):
        frappe.throw(_("Invalid SKU or Store ID"))

    se = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Material Issue",
        "items": [{
            "item_code": item,
            "qty": sold_qty,
            "s_warehouse": warehouse
        }]
    })
    se.insert(ignore_permissions=True)
    se.submit()
    return {"status": "success"}
