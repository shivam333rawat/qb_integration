app_name = "qb_integration"
app_title = "QB Integration"
app_publisher = "shivam333rawat"
app_description = "QueueBuster POS Integration for ERPNext"
app_email = "you@example.com"
app_license = "MIT"

doc_events = {
    "Stock Entry": {
        "on_submit": "qb_integration.sync.on_stock_submit"
    }
}

# fixtures = ["Custom Field"]  # uncomment if you export fields later

# Whitelisted methods (used for webhook)
override_whitelisted_methods = {}
