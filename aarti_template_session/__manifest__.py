# -*- coding: utf-8 -*-
{
    "name": "Template Session",
    "summary": """
        Demo module for template session""",
    "version": "14.0.1.0.0",
    "depends": ["website_sale"],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "data/partner_menu_website.xml",
        "data/product_menu_website.xml",
        "views/assets.xml",
        "views/partner_template.xml",
        "views/product_template.xml",
        "views/website_sale_template.xml",
        "views/res_partner.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
