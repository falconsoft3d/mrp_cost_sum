# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from collections import defaultdict

class McsStockMove(models.Model):
    _inherit = "stock.move"

    cost_price = fields.Float('Costo', readonly=True)

    #~ @api.multi
    #~ def product_price_update_before_done(self):
        #~ print 'product_price_update_before_done'
        #~ tmpl_dict = defaultdict(lambda: 0.0)
        #~ # adapt standard price on incomming moves if the product cost_method is 'average'
        #~ std_price_update = {}
        #~ for move in self.filtered(lambda move: move.location_id.usage in ('supplier', 'production') and move.product_id.cost_method == 'average'):
            #~ product_tot_qty_available = move.product_id.qty_available + tmpl_dict[move.product_id.id]
            #~ # if the incoming move is for a purchase order with foreign currency, need to call this to get the same value that the quant will use.
            #~ if product_tot_qty_available <= 0:
                #~ new_std_price = move.get_price_unit()
                #~ print 'cuandola cantidad actual es cero o menor, new_std_price',move.get_price_unit()
            #~ else:
                #~ # Get the standard price
                #~ amount_unit = std_price_update.get((move.company_id.id, move.product_id.id)) or move.product_id.standard_price
                #~ print 'disponible: %s | costo actual: %s | cant prod: %s | costo prod: %s'%(product_tot_qty_available, amount_unit, move.product_qty, move.get_price_unit())
                #~ new_std_price = ((amount_unit * product_tot_qty_available) + (move.get_price_unit() * move.product_qty)) / (product_tot_qty_available + move.product_qty)
                #~ print 'new_std_price....',new_std_price
#~ 
            #~ tmpl_dict[move.product_id.id] += move.product_qty
            #~ # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
            #~ move.product_id.with_context(force_company=move.company_id.id).sudo().write({'standard_price': new_std_price})
            #~ std_price_update[move.company_id.id, move.product_id.id] = new_std_price

    #~ @api.multi
    #~ def action_done(self):
        #~ for move in self:
            #~ if move.production_id:
                #~ move.cost_price = move.product_id.standard_price
                #~ print 'move.product_uom_qty ',move.product_uom_qty
                #~ print 'move.product_qty ',move.product_qty
                #~ print 'price_unit1',move.price_unit
                #~ if len(move.production_id.move_finished_ids) == 1:
                    #~ print 'cost_sum: ',(move.production_id.cost_sumatory / len(move.production_id.cost_lines))
                    #~ move.price_unit = len(move.production_id.cost_lines) > 0 and \
                        #~ (move.production_id.cost_sumatory / len(move.production_id.cost_lines))/move.product_uom_qty or 0.0
                #~ else:
                    #~ print 'cost_sum: ',sum(x.cost_price_unit for x in move.production_id.cost_lines if (x.move_id == move))
                    #~ move.price_unit = sum(x.cost_price_unit for x in move.production_id.cost_lines if (x.move_id == move))/move.product_uom_qty
                #~ 
        #~ return super(McsStockMove, self).action_done()
    
class McsStockQuant(models.Model):
    _inherit = "stock.quant"

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, journal_id):
        # group quants by cost
        quant_cost_qty = defaultdict(lambda: 0.0)
        for quant in self:
            quant_cost_qty[quant.cost] += quant.qty
        AccountMove = self.env['account.move']
        for cost, qty in quant_cost_qty.iteritems():
            move_lines = []
            if move.production_id:
                #~ cost_sum = 0.0
                #~ if len(move.production_id.move_finished_ids) == 1:
                    #~ cost_sum = move.production_id.cost_sumatory
                #~ else:
                    #~ cost_sum = sum(x.cost_price_unit for x in move.production_id.cost_lines if (x.move_id == move))
                move_lines = move.with_context(force_valuation_amount=move.price_unit)._prepare_account_move_line(\
                    qty, cost, credit_account_id, debit_account_id)
            else:
                move_lines = move._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
            if move_lines:
                date = self._context.get('force_period_date', fields.Date.context_today(self))
                ref = move.picking_id and move.picking_id.name or '%s - %s'%(move.name, move.product_id.name)
                new_account_move = AccountMove.create({
                    'journal_id': journal_id,
                    'line_ids': move_lines,
                    'date': date})
                new_account_move.post()
                new_account_move.write({'ref': ref})
