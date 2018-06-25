from odoo import fields, models

class McsWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    cost_hour = fields.Float(string='Costo por Hora', help="Especifica el costo del centro de trabajo por hora.", default=0.0)
