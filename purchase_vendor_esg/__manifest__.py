# -*- coding: utf-8 -*-
{
    'name': 'Vendor ESG & Sustainability Scorecard',
    'version': '18.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Track Vendor ESG Scores, Sustainability Certificates, Carbon Footprint & Audits',
    'sequence': 10,
    'author': "XodetiStudio",
    'website': "https://xodetistudio.id",
    'license': 'LGPL-3',

    'depends': ['base', 'purchase', 'purchase_stock', 'survey'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/esg_certificate_type_data.xml',
        'data/ir_cron_data.xml',
        'views/esg_certificate_type_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
        'views/res_config_settings_views.xml',
    ],

    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,

    'description': """
Vendor ESG & Sustainability Scorecard
=====================================
Transform your supply chain with active environmental, social, and corporate governance (ESG) risk management.
Engineered for Odoo 18.0 (Community & Enterprise).

Key Features:
-------------
1. **Hybrid Scoring Engine (0-100 pts)**
   - **Compliance (50%):** Validates mandatory certificates (e.g. ISO 14001, ISO 9001, OHSAS).
   - **Logistics Performance (30%):** Integrated with Odoo's native On-Time Delivery rate.
   - **Carbon Footprint / Proximity (20%):** Geolocation proximity calculation rewarding local suppliers (<100km).
   - **Audit Bonus:** Bonus points for verified Annual ESG Surveys.

2. **Active Risk Blocking (Smart PO)**
   - Proactively prevents confirming Purchase Orders with non-compliant ("Red") vendors.
   - Informative warning banners and audit trails.

3. **Operational Flexibility**
   - **Manager Override:** Permits managers to authorize emergency purchases with full audit logging.
   - **Global On/Off:** Toggle enforcement rules directly from Odoo Settings.

4. **Automated Auditing**
   - Integrated with Odoo Survey.
   - Auto-scheduled annual ESG questionnaires with scores pulled directly back into the Vendor record.

5. **Visual Indicators**
   - Green/Red ribbons on Vendor records, Kanban badges, and itemized score breakdowns.

100% Free and Open Source under LGPL-3 by XodetiStudio (https://xodetistudio.id).
    """,
}
