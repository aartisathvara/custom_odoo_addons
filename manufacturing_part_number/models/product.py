from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    manufacturing_part_number = fields.Char(String="Manufacturing Part Number")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    manufacturing_part_number = fields.Char(
        String="Manufacturing Part Number",
        compute="_compute_manufacturing_part_number",
        inverse="_set_manufacturing_part_number",
    )

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if vals.get("manufacturing_part_number"):
                related_vals["manufacturing_part_number"] = vals[
                    "manufacturing_part_number"
                ]
            if related_vals:
                template.write(related_vals)
        return templates

    @api.depends("product_variant_ids", "product_variant_ids.manufacturing_part_number")
    def _compute_manufacturing_part_number(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.manufacturing_part_number = (
                template.product_variant_ids.manufacturing_part_number
            )
        for template in self - unique_variants:
            template.manufacturing_part_number = False

    def _set_manufacturing_part_number(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.manufacturing_part_number = (
                    template.manufacturing_part_number
                )
