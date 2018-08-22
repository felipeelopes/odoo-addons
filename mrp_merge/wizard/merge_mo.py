# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import except_orm, Warning, RedirectWarning

class Merge_MO(models.TransientModel):
    _name = 'merge.mo'
    _description = 'Merged Manufacturing Order'

    @api.multi
    def merged_mo(self):
        mo_obj = self.env['mrp.production']
        mo_order_ids = mo_obj.browse(self.env.context['active_ids'])

        if not mo_order_ids or len(mo_order_ids) == 1:
            return 

        first_mo = mo_order_ids[0]
        second_mo = mo_order_ids[1]
        product_id = first_mo.product_id.id
        product_uom = first_mo.product_uom_id.id
        bom_id = first_mo.bom_id.id
        result = [mo for mo in mo_order_ids if mo.product_id.id <> product_id]
        result1 = [mo for mo in mo_order_ids if mo.product_uom_id.id <> product_uom]
        state_res = [mo for mo in mo_order_ids if mo.state <> 'confirmed']
        diff_bom_l = [mo for mo in mo_order_ids if mo.bom_id.id <> bom_id]

        if len(result):
            raise Warning('Diferença encontrada!\n\n Você só pode unificar ordens com a mesma estrutura.')
        if len(result1):
            raise Warning('Diferença encontrada na unidade de medida!\n\n Você poderá unir somente se as unidades de medidas das duas OP forem iguais.')
        if len(state_res):
            raise Warning('Diferença encontrada no estado da OP!\n\n Você poderá unir somente OP com o estado confirmado.')
        if len(diff_bom_l):
            raise Warning('Diferença encontrada na matéria prima!\n\n Ambas as OP devem possuir a mesma lista de matéria prima.')

        total_qty = 0
        new_mo = mo_order_ids[0].copy()
        ref = ''

        # Atualizar quantidade de materia prima necessaria, somando as duas ordens de producao
        for bom_old in second_mo.move_raw_ids:
            for bom_new in new_mo.move_raw_ids:
                if bom_new.product_id == bom_old.product_id:
                    bom_new.product_uom_qty += bom_old.product_uom_qty

        # Atualizar quantidade da mercadoria a ser prodizida
        for mo in mo_order_ids:
            total_qty += mo.product_qty
            if not ref:
                ref = mo.name
            else:
                ref += str(mo.origin)
            mo.write({'state':'cancel'})

        new_mo.write({'product_qty':total_qty, 'origin': ref})