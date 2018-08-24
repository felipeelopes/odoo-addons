# -*- coding: utf-8 -*-

from odoo import fields, models

class EpiBom(models.Model):
    _inherit = 'mrp.bom' 
    
    epi_field = fields.Text(string='Epis necessários', help='Adicione neste campo todos os EPIs necessários no manuseio das matérias primar contidas nessa lista.')