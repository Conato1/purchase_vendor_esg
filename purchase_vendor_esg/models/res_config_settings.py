# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # --- 1. GLOBAL ON/OFF CHECKING ---
    # Saya menghapus config_parameter=... dari field definition
    # Kita akan handle manual di get_values/set_values agar 100% akurat
    group_esg_validation = fields.Boolean(
        string="Enable ESG Blocking",
        implied_group='purchase_vendor_esg.group_esg_manager', 
        help="If unchecked, the ESG logic will be disabled globally (no PO blocking)."
    )

    # --- 2. SURVEY AUTOMATION SETTINGS ---
    esg_auto_survey = fields.Boolean(
        string="Auto Send Annual Survey",
        config_parameter='purchase_vendor_esg.auto_survey',
        help="If active, system will automatically send survey on the specific date."
    )

    esg_survey_month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string="Schedule Month", default='1', config_parameter='purchase_vendor_esg.survey_month')

    esg_survey_day = fields.Integer(
        string="Schedule Day", 
        default=1, 
        config_parameter='purchase_vendor_esg.survey_day',
        help="Day of the month to trigger the survey (e.g., 1 for 1st of January)."
    )

    esg_default_survey_id = fields.Many2one(
        'survey.survey',
        string="Default ESG Survey",
        config_parameter='purchase_vendor_esg.default_survey_id',
        help="The standard survey questionnaire to be sent to all vendors."
    )
    
    # --- MANUAL SAVE & LOAD LOGIC (CRUCIAL FIX) ---
    
    @api.model
    def get_values(self):
        """ Mengambil data dari database saat menu dibuka """
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        
        # 1. Ambil status Blocking (Manual Read)
        # Hati-hati: config param menyimpan string "True"/"False", bukan boolean
        enable_blocking = params.get_param('purchase_vendor_esg.enable_blocking', default='False')
        
        # 2. Ambil Survey ID
        survey_id = params.get_param('purchase_vendor_esg.default_survey_id')
        
        # Update nilai untuk ditampilkan di Form
        res.update(
            group_esg_validation=(enable_blocking == 'True'),
            esg_default_survey_id=int(survey_id) if survey_id else False,
        )
        return res

    def set_values(self):
        """ Menyimpan data ke database saat tombol Save ditekan """
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        
        # 1. Simpan status Blocking (Manual Write)
        # Kita simpan sebagai string 'True' atau 'False' agar konsisten
        params.set_param('purchase_vendor_esg.enable_blocking', str(self.group_esg_validation))
        
        # 2. Simpan Survey ID (sudah dihandle config_parameter tapi kita pastikan ulang)
        params.set_param('purchase_vendor_esg.default_survey_id', self.esg_default_survey_id.id or False)