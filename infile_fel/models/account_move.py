# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
from datetime import datetime
import pytz
import uuid

class infilefel_account_move(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    infilefel_export = fields.Boolean('Export invoice')
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['infilefel_uuid'] = str(uuid.uuid4())
        ret = super(infilefel_account_move, self).create(vals_list)
        return ret

    def _post(self, soft=True):
        for invoice in self:
            if invoice.journal_id.infilefel_type and invoice.journal_id.infilefel_type != '':
                if not invoice.invoice_date:
                    invoice.invoice_date = datetime.now().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(self.env.user.tz))
                if not invoice.invoice_date:
                    raise UserError(_('Missing document date'))
                else:
                    if not invoice.infilefel_uuid:
                        invoice.infilefel_uuid = str(uuid.uuid4())
                    if invoice.infilefel_uuid.strip() == '':
                        invoice.infilefel_uuid = str(uuid.uuid4())
        ret = super(infilefel_account_move, self)._post(soft)
        if ret:
            settings = self.env['infilefel.settings'].search([])
            if settings:
                for invoice in self:
                    if invoice.journal_id.infilefel_type and invoice.journal_id.infilefel_type != '':
                        settings.sign_document(invoice)
        return ret

    def infilefel_move_void(self):
        settings = self.env['infilefel.settings'].search([])
        if settings:
            for inv in self:
                if inv.journal_id.infilefel_type and inv.journal_id.infilefel_type != '':
                    if inv.infilefel_sat_uuid:
                        settings.void_document(inv)
        return True
