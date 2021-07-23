# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class infilefel_account_tax(models.Model):
    _name = "account.tax"
    _inherit = "account.tax"

    infilefel_sat_code = fields.Char('SAT Code')
    infile_tax_type = fields.Char('Tax type')
