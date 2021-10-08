# -*- coding: utf-8 -*-
{
    "name": "Customer Document",
    "summary": """This module use for customer document details""",
    "description": """This module customer can create and view document details.""",
    "author": "Aarti Sathvara",
    "website": "https://www.aktivsoftware.com",
    "category": "Document",
    "version": "14.0.1.0.0",
    "depends": ["website"],
    "data": [
        "security/ir.model.access.csv",
        "data/customer_document_menu.xml",
        "views/customer_document.xml",
        "views/customer_document_template.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
