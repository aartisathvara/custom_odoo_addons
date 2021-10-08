from odoo i/home/admin123/Aarti/odoo_workspacemport api, models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    my_name = fields.Char('My Name')

    def name_get(self):
        result = []
        if self._context.get("partner_id"):
            for partner in self:
                result.append((partner.id, "%s (%s) (%s)" % (partner.name, partner.city, partner.state_id.name)))
            return result
        return super(ResPartner, self).name_get()

    @api.model
    def _name_search(self, name="", args=None, operator="ilike", limit=100):
        if self._context.get("partner_id"):
            if args is None:
                args = []
            domain = args + ["|", ("name", operator, name), ("city", operator, name)]
            return super(ResPartner, self)._search(domain, limit=limit)


