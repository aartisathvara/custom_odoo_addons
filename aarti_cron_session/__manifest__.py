{
    "name": "Sale Order Cron Job",
    "summary": """Sale module for cron session""",
    "version": "14.0.1.0.0",
    "depends": ["sale_management"],
    "license": "AGPL-3",
    "data": [
        "data/invoice_mail_cron.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
