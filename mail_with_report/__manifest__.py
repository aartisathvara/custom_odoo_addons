{
    "name": "Mail With Report",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "summary": "Mail With Report",
    "sequence": 1,
    "description": """This module contains inherit sale order report and mail template with cron""",
    "depends": ["sale_management", "stock", "delivery"],
    "data": [
        "report/sale_report.xml",
        "data/invoice_mail_template.xml",
        "report/sale_order_report_inherit.xml",
        "views/sale.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
