# -*- coding: utf-8 -*-
{
    "name": "purchase_append",
    "summary": """Purchase Append""",
    "description": """Purchase Append""",
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "0.purchase_append",
    "depends": ["base", "purchase", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/referral_program_menu.xml",
        "views/purchase_order.xml",
        "views/sale_order_template.xml",
        "views/res_partner.xml",
        "views/tracking_order_views.xml",
    ],
}
