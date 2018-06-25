# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round

class McsMrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.multi
    def do_produce(self):
        # Nothing to do for lots since values are created using default data (stock.move.lots)
        moves = self.production_id.move_raw_ids
        quantity = self.product_qty
        qty_consumed = {}
        if quantity > self.production_id.product_qty:
            raise ValidationError('La cantidad ingresada excede a la cantidad a producir en la Orden de Producción')
        if moves and any([x.state == 'draft' for x in moves]):
            raise ValidationError('Hay movimientos de insumos no confirmados')
        if float_compare(quantity, 0, precision_rounding=self.product_uom_id.rounding) <= 0:
            raise UserError(_('You should at least produce some quantity'))
        for move in moves.filtered(lambda x: x.product_id.tracking == 'none' and x.state not in ('done', 'cancel')):
            if move.unit_factor:
                qty_consumed[move.product_id.id] = move.quantity_done
                rounding = move.product_uom.rounding
                move.quantity_done_store += float_round(quantity * move.unit_factor, precision_rounding=rounding)
        moves = self.production_id.move_finished_ids.filtered(lambda x: x.product_id.tracking == 'none' and x.state not in ('done', 'cancel'))
        for move in moves:
            rounding = move.product_uom.rounding
            if move.product_id.id == self.production_id.product_id.id:
                move.quantity_done_store += float_round(quantity, precision_rounding=rounding)
            elif move.unit_factor:
                # byproducts handling
                move.quantity_done_store += float_round(quantity * move.unit_factor, precision_rounding=rounding)
            #~ cost_price_unit = sum(x.product_id.standard_price*(x.quantity_done_store - qty_consumed[x.product_id.id]) for x in self.production_id.move_raw_ids if(x.state != 'done'))
            #~ self.env['mrp.production.cost.line'].create({
                #~ 'product_id': self.production_id.product_id.id,
                #~ 'quantity': quantity,
                #~ 'cost_price_unit': cost_price_unit,
                #~ 'cost_total': quantity*cost_price_unit,
                #~ 'production_id': self.production_id.id,
                #~ 'move_id': move.id
            #~ })
        self.check_finished_move_lots()
        if self.production_id.state == 'confirmed':
            self.production_id.write({
                'state': 'progress',
                'date_start': datetime.now(),
            })
        return {'type': 'ir.actions.act_window_close'}
