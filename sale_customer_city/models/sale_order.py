from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def name_get(self):
        result = []
        if self._context.get("partner_id"):
            for partner in self:
                result.append((partner.id, "%s (%s)" % (partner.name, partner.city)))
            return result
        return super(ResPartner, self).name_get()

    @api.model
    def _name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        domain = args + ["|", ("name", operator, name), ("city", operator, name)]
        return super(ResPartner, self)._search(domain, limit=limit)
