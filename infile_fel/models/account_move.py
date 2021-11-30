# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import uuid

class infilefel_account_move(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    infilefel_export = fields.Boolean('Export')
    infilefel_uuid = fields.Char('Document UUID', copy=False)
    infilefel_sat_uuid = fields.Char('SAT UUID', copy=False)
    infilefel_source_xml = fields.Text('Source XML', copy=False)
    infilefel_signed_xml = fields.Text('Signed XML', copy=False)
    infilefel_result_xml = fields.Text('Result XML', copy=False)
    infilefel_void_uuid = fields.Char('Void document UUID', copy=False)
    infilefel_void_sat_uuid = fields.Char('Void SAT UUID', copy=False)
    infilefel_void_source_xml = fields.Text('Void source XML', copy=False)
    infilefel_void_signed_xml = fields.Text('Void signed XML', copy=False)
    infilefel_void_result_xml = fields.Text('Void result XML', copy=False)
    infilefel_sign_date = fields.Datetime('Sign date', copy=False)
    infilefel_serial = fields.Text('SAT invoice serial', copy=False)
    infilefel_number = fields.Text('SAT invoice number', copy=False)
    infilefel_vat = fields.Text('SAT person VAT', copy=False)
    infilefel_name = fields.Text('SAT person name', copy=False)
    infilefel_address = fields.Text('SAT person address', copy=False)

    # def action_post(self):
    #     settings = self.env['infilefel.settings'].search([])
    #     if settings:
    #         settings.sign_document(self)
    #     ret = super(infilefel_account_move, self).action_post()
    #     if ret:
    #         if self.journal_id.infilefel_type and self.journal_id.infilefel_type != '':
    #             self.write({ 'name': '{}-{}'.format(self.infilefel_serial, self.infilefel_number), })
    #     return ret

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['infilefel_uuid'] = str(uuid.uuid4())
        ret = super(infilefel_account_move, self).create(vals_list)
        return ret

    def _post(self, soft=True):
        for invoice in self:
            if not invoice.infilefel_uuid:
                invoice.infilefel_uuid = str(uuid.uuid4())
            if invoice.infilefel_uuid.strip() == '':
                invoice.infilefel_uuid = str(uuid.uuid4())
        ret = super(infilefel_account_move, self)._post(soft)
        if ret:
            settings = self.env['infilefel.settings'].search([])
            if settings:
                for invoice in self:
                    settings.sign_document(invoice)
                    if invoice.journal_id.infilefel_type and invoice.journal_id.infilefel_type != '':
                        invoice.write({ 'name': '{}-{}'.format(invoice.infilefel_serial, invoice.infilefel_number), })
        return ret

    def infilefel_move_void(self):
        settings = self.env['infilefel.settings'].search([])
        for inv in self:
            if inv.infilefel_sat_uuid:
                settings.void_document(inv)
        return True
