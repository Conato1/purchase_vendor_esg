# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from math import radians, cos, sin, asin, sqrt
from datetime import timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # --- ESG Fields ---
    esg_certificate_ids = fields.One2many(
        'esg.certificate', 
        'partner_id', 
        string='ESG Certificates'
    )
    
    # --- AUDIT / SURVEY FIELDS ---
    audit_survey_id = fields.Many2one(
        'survey.survey', 
        string="Active Audit Survey",
        help="Select the questionnaire to be sent to this vendor."
    )
    
    audit_last_date = fields.Date(
        string="Last Audit Date", 
        readonly=True,
        help="Date of the last completed survey."
    )
    
    audit_score = fields.Float(
        string="Audit Score (%)", 
        readonly=True, 
        aggregator="avg", # PERBAIKAN: Odoo 18 menggunakan aggregator, bukan group_operator
        help="Score obtained in the last ESG Survey."
    )

    # --- SCORING & COMPLIANCE ---
    esg_score = fields.Float(
        string='Total Sustainability Score', 
        compute='_compute_esg_status', 
        store=False, 
        help="Total Score derived from:\n"
             "1. Compliance (Certificates)\n"
             "2. Performance (On-Time Delivery)\n"
             "3. Proximity (Local vs Import)\n"
             "4. Audit Result (Survey Score)"
    )
    
    is_esg_compliant = fields.Boolean(
        string='ESG Compliant', 
        compute='_compute_esg_status', 
        store=False,
        help="Vendor is compliant if they have mandatory certs AND pass the audit."
    )

    # --- ACTIONS ---
    def action_send_esg_survey(self):
        """ Button to send the selected survey to the vendor """
        self.ensure_one()
        if not self.audit_survey_id:
            # Fallback: Try to find a survey named 'ESG' if none selected
            survey = self.env['survey.survey'].search([('title', 'ilike', 'ESG')], limit=1)
            if survey:
                self.audit_survey_id = survey.id
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('No Survey Selected'),
                        'message': _('Please create or select an ESG Survey first.'),
                        'type': 'warning',
                        'sticky': False,
                    }
                }
        
        # Open the standard Odoo Survey Share Wizard
        return self.audit_survey_id.action_send_survey()

    # --- CRON JOB LOGIC ---
    @api.model
    def _cron_send_annual_surveys(self):
        """ This method is called by the Scheduled Action (Cron) """
        params = self.env['ir.config_parameter'].sudo()
        
        # 1. Cek apakah fitur Auto Survey Aktif?
        is_auto = params.get_param('purchase_vendor_esg.auto_survey')
        if not is_auto:
            return # Fitur mati, berhenti.

        # 2. Cek apakah Hari ini = Jadwal Pengiriman?
        cfg_month = int(params.get_param('purchase_vendor_esg.survey_month', '1'))
        cfg_day = int(params.get_param('purchase_vendor_esg.survey_day', '1'))
        today = fields.Date.today()
        
        if today.month != cfg_month or today.day != cfg_day:
            return # Bukan hari ulang tahun survey, berhenti.

        # 3. Ambil Default Survey ID
        survey_id = int(params.get_param('purchase_vendor_esg.default_survey_id', '0'))
        if not survey_id:
            return # Tidak ada template survey dipilih.

        survey_obj = self.env['survey.survey'].browse(survey_id)
        if not survey_obj.exists():
            return

        # 4. Cari Vendor Aktif
        vendors = self.search([
            ('supplier_rank', '>', 0),
            ('active', '=', True),
            ('email', '!=', False) 
        ])

        sent_count = 0
        for vendor in vendors:
            last_valid_date = today - timedelta(days=300)
            existing_input = self.env['survey.user_input'].search([
                ('partner_id', '=', vendor.id),
                ('survey_id', '=', survey_id),
                ('create_date', '>', last_valid_date)
            ], limit=1)

            if not existing_input:
                response = survey_obj._create_answer(partner=vendor)
                template = self.env.ref('survey.mail_template_user_input_invite', raise_if_not_found=False)
                if template:
                    template.send_mail(response.id, force_send=True)
                    sent_count += 1
                    vendor.audit_survey_id = survey_obj.id

        print(f"ESG AUTO SURVEY: Sent {sent_count} emails to vendors.")

    # --- Helper: Haversine Formula for Distance (KM) ---
    def _get_distance_km(self, lat1, lon1, lat2, lon2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 
        return c * r

    def _get_latest_survey_score(self):
        """ Fetch the latest completed survey score for this partner """
        for partner in self:
            domain = [
                ('partner_id', '=', partner.id),
                ('state', '=', 'done')
            ]
            if partner.audit_survey_id:
                domain.append(('survey_id', '=', partner.audit_survey_id.id))
            
            last_input = self.env['survey.user_input'].search(domain, order='create_date desc', limit=1)
            
            if last_input:
                partner.audit_last_date = last_input.create_date.date()
                partner.audit_score = last_input.scoring_percentage
                return last_input.scoring_percentage
            else:
                partner.audit_last_date = False
                partner.audit_score = 0.0
                return 0.0

    # --- Compute Logic ---
    @api.depends('esg_certificate_ids', 'esg_certificate_ids.state', 
                 'esg_certificate_ids.certificate_type_id', 
                 'country_id', 'state_id', 'partner_latitude', 'partner_longitude',
                 'audit_survey_id') 
    def _compute_esg_status(self):
        # 1. Fetch mandatory types
        mandatory_types = self.env['esg.certificate.type'].search([('is_mandatory', '=', True)])
        mandatory_type_ids = mandatory_types.ids
        
        # Get Current Company for Location Comparison
        company = self.env.company.partner_id

        for partner in self:
            # === PART A: CERTIFICATE SCORING ===
            cert_score = 0.0
            valid_type_ids = []
            for cert in partner.esg_certificate_ids:
                is_valid_now = cert.state == 'valid'
                if cert.date_start and cert.date_end:
                    today = fields.Date.today()
                    if cert.date_start <= today <= cert.date_end:
                        is_valid_now = True
                    else:
                        is_valid_now = False
                if is_valid_now:
                    cert_score += cert.certificate_type_id.score_weight
                    valid_type_ids.append(cert.certificate_type_id.id)

            # === PART B: LOGISTICS PERFORMANCE (SAFE MODE) ===
            performance_score = 0.0
            on_time_val = getattr(partner, 'on_time_rate', -1)
            if on_time_val >= 0:
                performance_score = on_time_val * 0.3 

            # === PART C: LOCATION SCORING ===
            location_score = 0.0
            has_gps = (partner.partner_latitude and partner.partner_longitude and 
                       company.partner_latitude and company.partner_longitude)
            if has_gps:
                dist = self._get_distance_km(company.partner_latitude, company.partner_longitude,
                                             partner.partner_latitude, partner.partner_longitude)
                if dist < 100: location_score = 20.0
                elif dist < 1000: location_score = 10.0
            else:
                if partner.country_id and company.country_id:
                    if partner.country_id == company.country_id:
                        if partner.state_id and company.state_id and partner.state_id == company.state_id:
                            location_score = 20.0
                        else:
                            location_score = 10.0

            # === PART D: AUDIT SURVEY SCORING ===
            audit_percentage = partner._get_latest_survey_score() 
            audit_points = (audit_percentage / 100.0) * 20.0 

            # === FINAL CALCULATION ===
            partner.esg_score = cert_score + performance_score + location_score + audit_points

            # === COMPLIANCE CHECK ===
            if not mandatory_type_ids:
                has_docs = True
            else:
                has_docs = set(mandatory_type_ids).issubset(set(valid_type_ids))
            
            audit_pass = True
            if partner.audit_survey_id and partner.audit_last_date:
                if audit_percentage < 50.0:
                    audit_pass = False
            
            partner.is_esg_compliant = has_docs and audit_pass