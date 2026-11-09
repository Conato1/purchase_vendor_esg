# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EsgCertificateType(models.Model):
    _name = 'esg.certificate.type'
    _description = 'ESG Certificate Type'
    _order = 'sequence, id'

    name = fields.Char(
        string='Certificate Name', 
        required=True, 
        translate=True,
        help="Name of the certification (e.g., ISO 14001, Fair Trade)."
    )
    code = fields.Char(
        string='Code', 
        required=True,
        help="Unique code for internal reference."
    )
    sequence = fields.Integer(
        string='Sequence', 
        default=10
    )
    active = fields.Boolean(
        string='Active', 
        default=True
    )

    # --- Scoring & Compliance Logic ---
    score_weight = fields.Float(
        string='Score Weight', 
        default=10.0, 
        required=True,
        help="Points awarded to the vendor if they possess this valid certificate. Total ESG score is the sum of these weights."
    )
    is_mandatory = fields.Boolean(
        string='Mandatory for PO', 
        default=False, 
        help="If checked, Purchase Orders to a vendor will be blocked/warned if they do not have this valid certificate."
    )

    description = fields.Text(
        string='Description', 
        translate=True
    )

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The code of the certificate type must be unique!'),
        ('name_uniq', 'unique (name)', 'The name of the certificate type must be unique!'),
    ]