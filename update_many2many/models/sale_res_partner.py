# -*- coding: utf-8 -*-
"""
(0, 0, { values }) -- link to a new record that needs to be created with the given values dictionary
(1, ID, { values }) -- update the linked record with id = ID (write values on it)
(2, ID) -- remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
(3, ID) -- cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
(4, ID) -- link to existing record with id = ID (adds a relationship)
(5) -- unlink all (like using (3,ID) for all linked records)
(6, 0, [IDs]) -- replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
"""
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    custom_partner_ids = fields.Many2many(
        "res.partner", "sale_partner_rel", "sale_id", "partner_id", string="Partner"
    )
    custom_product_id = fields.Many2one('product.template',string="Product")


    @api.onchange("custom_product_id")
    def order_line_add_variant(self):
        for product_variant_id in self.custom_product_id.product_variant_ids:
            print(product_variant_id)
            self.write({"order_line": [(0, 0,
                    {
                        "product_id": product_variant_id,
                        "name":product_variant_id.name,
                        "product_uom_qty":5.0,
                        "price_unit":product_variant_id.lst_price,
                        "product_uom":product_variant_id.uom_id.id
                    }
                                        )]})

    def update_many2many(self):
        print("\n\n update many2mnay")
        print("==",self)
        print(self.read())
        """(0, 0, { values }) -- link to a new record that needs to be created with the given values dictionary"""
        # partner_list = []
        # for partner in range(1, 11):
        #     partner_dict = {"name": partner, "phone": 123456789}
        #     partner_list.append(partner_dict)
        # for val in partner_list:
        #     self.custom_partner_ids = [(0, 0, val)]

        """(1, ID, { values }) -- update the linked record with id = ID (write values on it)"""
        # self.custom_partner_ids = [(1, 43, {"phone": "8460232337"})]

        """(2, ID) -- remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)"""
        # self.custom_partner_ids = [(2, 44)]

        """(3, ID) -- cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)"""
        # self.custom_partner_ids = [(3, 45)]

        """(4, ID) -- link to existing record with id = ID (adds a relationship)"""
        # self.custom_partner_ids = [(4, 26)]

        """(5) -- unlink all (like using (3,ID) for all linked records)"""
        # self.custom_partner_ids = [(5,)]

        """(6, 0, [IDs]) -- replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)"""
        # self.custom_partner_ids = [(6, 0, [11, 23])]

