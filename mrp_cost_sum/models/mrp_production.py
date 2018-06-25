# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class McsProductionWorkcenterLineTime(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    cost_already_recorded = fields.Boolean('Cost Almacendao', help="Se verifica automáticamente cuando una producción en curso publica las entradas del diario por sus costos. De esta forma, podemos registrar el costo de una producción varias veces y solo considerar nuevas entradas en las líneas de tiempo de los centros de trabajo.")

class McsMrpProduction(models.Model):
    _inherit = 'mrp.production'

    #~ @api.multi
    #~ def compute_cost_sumatory(self):
        #~ for production in self:
            #~ production.cost_sumatory = sum(x.cost_total for x in production.cost_lines)

    #~ cost_sumatory = fields.Float('Sumatoria de costos', help="Sumatoria de costos de los insumos",
        #~ compute="compute_cost_sumatory", digits=dp.get_precision('Product Price'))
    #~ cost_lines = fields.One2many('mrp.production.cost.line', 'production_id','Costos por producción')
    currency_id = fields.Many2one('res.currency','Moneda', related="company_id.currency_id")

    def _cal_price(self, consumed_moves):
        """Set a price unit on the finished move according to `consumed_moves`.
        """
        super(McsMrpProduction, self)._cal_price(consumed_moves)
        work_center_cost = 0
        finished_move = self.move_finished_ids.filtered(lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel') and x.quantity_done > 0)
        #~ print 'Costeo:',finished_move.product_id.cost_method
        #~ for q in consumed_moves.mapped('quant_ids').filtered(lambda x: x.qty > 0.0):
            #~ print 'product: %s | quantity: %s | invetory_value: %s | standard_price: %s'%(q.product_id.name, q.qty, q.inventory_value, q.product_id.standard_price)
        if finished_move:
            finished_move.ensure_one()
            for work_order in self.workorder_ids:
                time_lines = work_order.time_ids.filtered(lambda x: x.date_end and not x.cost_already_recorded)
                duration = sum(time_lines.mapped('duration'))
                time_lines.write({'cost_already_recorded': True})
                work_center_cost += (duration / 60.0) * work_order.workcenter_id.cost_hour
            if finished_move.product_id.cost_method in ('real', 'average'):
                #~ print 'Suma de Insumo',(sum([q.product_id.standard_price*q.qty for q in consumed_moves.mapped('quant_ids').filtered(lambda x: x.qty > 0.0)]))
                finished_move.price_unit = (sum([q.product_id.standard_price*q.qty for q in consumed_moves.mapped('quant_ids').filtered(lambda x: x.qty > 0.0)]) + work_center_cost) / finished_move.quantity_done
        return True

#~ class MrpProductionCostLine(models.Model):
    #~ _name = 'mrp.production.cost.line'
    #~ _description = 'Costo por oleada de produccion'
#~ 
    #~ production_id = fields.Many2one('mrp.production','Orden de Producción')
    #~ move_id = fields.Many2one('stock.move','Movimiento')
    #~ product_id = fields.Many2one('product.product','Producto')
    #~ quantity = fields.Float('Cantidad Producida')
    #~ cost_price_unit = fields.Float('Costo Unitario', digits=dp.get_precision('Product Price'))
    #~ cost_total = fields.Float('Costo de Producción', digits=dp.get_precision('Product Price'))
