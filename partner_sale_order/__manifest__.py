{
    "name": "Partner Sale Order",
    "summary": """Partner Sale Order""",
    "version": "14.0.purchase_append.0.0",
    "depends": ["sale_management"],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "report/sale_order_template.xml",
        "wizard/create_sale_order_wizard.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
