# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import except_orm, Warning, RedirectWarning

class EpiBom(models.Model):
    _inherit = 'mrp.bom' 
    epi_field = fields.Text(string='Epis necessários')