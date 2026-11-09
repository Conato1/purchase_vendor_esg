# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # --- ESG Indicators for PO View ---
    partner_esg_score = fields.Float(
        related='partner_id.esg_score', 
        string='Vendor ESG Score', 
        readonly=True
    )
    
    partner_esg_compliant = fields.Boolean(
        related='partner_id.is_esg_compliant', 
        string='Vendor ESG Compliant', 
        readonly=True
    )

    # --- Override Switch ---
    ignore_esg_check = fields.Boolean(
        string="Ignore ESG Warning",
        default=False,
        tracking=True, 
        help="If checked, allows confirming the PO even if the vendor is not ESG compliant."
    )

    def button_confirm(self):
        """
        Override confirm button to block POs for non-compliant vendors,
        UNLESS the 'Ignore ESG Warning' switch is active.
        """
        # 1. Bypass saat Install Module / Demo Data loading
        if self.env.context.get('install_mode'):
            return super(PurchaseOrder, self).button_confirm()

        # 2. Cek Global Setting dari Database
        # Kita ambil parameter sebagai string untuk keamanan perbandingan
        param = self.env['ir.config_parameter'].sudo().get_param('purchase_vendor_esg.enable_blocking')
        enable_blocking = str(param).lower() == 'true'

        # Jika fitur dimatikan di setting, langsung lolos (Standard Odoo Behavior)
        if not enable_blocking:
            return super(PurchaseOrder, self).button_confirm()

        # 3. Pengecekan Per-Order (Strict Mode)
        for order in self:
            # Skip jika tidak ada vendor
            if not order.partner_id:
                continue

            # LOGIKA UTAMA:
            # Blokir jika: (Tidak Patuh) DAN (Tidak di-Bypass oleh Manager)
            if not order.partner_esg_compliant and not order.ignore_esg_check:
                
                # Pesan Error Profesional
                msg = _(
                    "Action Blocked: ESG Compliance Check Failed.\n\n"
                    "The vendor '%s' does not meet the mandatory ESG requirements.\n"
                    "Current ESG Score: %s\n\n"
                    "To proceed with this Purchase, please enable 'Ignore ESG Warning' (Manager Only) or update vendor certificates."
                ) % (order.partner_id.name, order.partner_esg_score)
                
                raise UserError(msg)

        # Jika lolos semua cek, jalankan fungsi standar Odoo
        return super(PurchaseOrder, self).button_confirm()