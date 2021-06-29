# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class infilefel_account_journal(models.Model):
    _name = "account.journal"
    _inherit = "account.journal"

    infilefel_type = fields.Selection([
        ('', ''),
        ('FACT', 'FACT'),
        ('FCAM', 'FCAM'),
        ('FPEQ', 'FPEQ'),
        ('FCAP', 'FCAP'),
        ('FESP', 'FESP'),
        ('NABN', 'NABN'),
        ('RDON', 'RDON'),
        ('RECI', 'RECI'),
        ('NDEB', 'NDEB'),
        ('NCRE', 'NCRE'),
    ], string='FEL Invoice type', default='')
    infilefel_previous_authorization = fields.Char('Previous invoice authorization')
    infilefel_previous_serial = fields.Char('Previous invoice serial')
    infilefel_organization_code = fields.Char('Organization code', default='1')
    infilefel_vat_affiliation = fields.Selection([
        ('GEN', 'GEN'),
        ('EXE', 'EXE'),
        ('PEQ', 'PEQ'),
    ], string='VAT affiliation', default='GEN')
    infilefel_isr_scenery = fields.Char('ISR sceneries')
    infilefel_isr_phrases = fields.Char('ISR phrases')
    infilefel_person_type = fields.Char('Person type')
