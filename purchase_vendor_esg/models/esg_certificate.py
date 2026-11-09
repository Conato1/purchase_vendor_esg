# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class EsgCertificate(models.Model):
    _name = 'esg.certificate'
    _description = 'Vendor ESG Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'certificate_type_id'
    _order = 'date_end desc'

    partner_id = fields.Many2one(
        'res.partner', 
        string='Vendor', 
        required=True, 
        ondelete='cascade',
        tracking=True,
        domain="[('supplier_rank', '>', 0)]",
        help="The vendor associated with this certificate."
    )
    certificate_type_id = fields.Many2one(
        'esg.certificate.type', 
        string='Certificate Type', 
        required=True,
        tracking=True
    )
    certificate_reference = fields.Char(
        string='Reference Number',
        help="The official ID number listed on the certificate document."
    )
    
    # --- Dates ---
    date_start = fields.Date(
        string='Issue Date', 
        required=True, 
        default=fields.Date.today,
        tracking=True
    )
    date_end = fields.Date(
        string='Expiry Date', 
        required=True,
        tracking=True
    )
    
    # --- Documents ---
    certificate_file = fields.Binary(
        string='Certificate Document', 
        attachment=True,
        help="Upload the scanned PDF or Image of the certificate."
    )
    filename = fields.Char(string='Filename')

    # --- Computed Status ---
    state = fields.Selection([
        ('draft', 'Draft'),
        ('valid', 'Valid'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], string='Status', compute='_compute_state', store=True, tracking=True)

    days_to_expire = fields.Integer(
        string='Days to Expire', 
        compute='_compute_days_to_expire',
        help="Days remaining until the certificate expires."
    )

    # --- Logic ---

    @api.depends('date_end')
    def _compute_days_to_expire(self):
        for record in self:
            if record.date_end:
                delta = record.date_end - fields.Date.today()
                record.days_to_expire = delta.days
            else:
                record.days_to_expire = 0

    @api.depends('date_start', 'date_end')
    def _compute_state(self):
        today = fields.Date.today()
        warning_threshold = 30  # Days to warn before expiry
        
        for record in self:
            if not record.date_start or not record.date_end:
                record.state = 'draft'
                continue

            if record.date_end < today:
                record.state = 'expired'
            elif 0 <= (record.date_end - today).days <= warning_threshold:
                record.state = 'expiring'
            elif record.date_start > today:
                record.state = 'draft' # Issued in future?
            else:
                record.state = 'valid'

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError(_("The Issue Date cannot be later than the Expiry Date."))

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.certificate_type_id.name} - {record.partner_id.name}"
            result.append((record.id, name))
        return result