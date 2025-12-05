import frappe
import requests

def on_stock_submit(doc, method):
    for d in doc.items:
        item = frappe.get_doc("Item", d.item_code)
        warehouse = frappe.get_doc("Warehouse", d.t_warehouse or d.s_warehouse)

        qb_sku = item.get("qb_sku")
        qb_store_id = warehouse.get("qb_store_id")

        if not (qb_sku and qb_store_id):
            frappe.log_error(f"Missing QB mapping for Item {item.name} or Warehouse {warehouse.name}", "QB Sync")
            continue

        bin = frappe.get_doc("Bin", {"item_code": item.name, "warehouse": warehouse.name})
        qty = bin.actual_qty

        payload = {
            "sku": qb_sku,
            "store_id": qb_store_id,
            "quantity": qty
        }

        headers = {
            "Authorization": f"Bearer {frappe.conf.get('qb_api_key')}",
            "Content-Type": "application/json"
        }

        url = "https://api.queuebuster.co/inventory/update"  # Replace with actual QB endpoint

        try:
            res = requests.post(url, json=payload, headers=headers)
            res.raise_for_status()
            frappe.get_doc({
                "doctype": "QB Sync Log",
                "reference_type": "Stock Entry",
                "reference_name": doc.name,
                "qb_id": qb_sku + "/" + qb_store_id,
                "status": "Success",
                "message": f"Synced Qty: {qty}"
            }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"QB Sync Failed: {e}", "QB Integration")
            frappe.get_doc({
                "doctype": "QB Sync Log",
                "reference_type": "Stock Entry",
                "reference_name": doc.name,
                "qb_id": qb_sku + "/" + qb_store_id,
                "status": "Failed",
                "message": str(e)
            }).insert(ignore_permissions=True)

