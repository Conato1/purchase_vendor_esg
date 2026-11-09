# Vendor ESG & Sustainability Scorecard for Odoo 18.0

[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-714B67.svg?style=flat-square&logo=odoo&logoColor=white)](https://www.odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/lgpl-3.0)
[![Author: XodetiStudio](https://img.shields.io/badge/Author-XodetiStudio-06b6d4.svg?style=flat-square)](https://xodetistudio.id)
[![Category](https://img.shields.io/badge/Category-Purchases%20%2F%20ESG-orange.svg?style=flat-square)](https://xodetistudio.id)

A proactive Environmental, Social, and Governance (ESG) supply chain risk management module for **Odoo 18.0 (Community & Enterprise)**. Scores suppliers, validates ISO certificates, calculates carbon footprint proximity, and intercepts non-compliant Purchase Orders. Distributed **100% Free and Open Source** under the LGPL-3 license by **[XodetiStudio](https://xodetistudio.id)**.

---

## 🌟 Key Features

1. **Hybrid Scoring Engine (0&ndash;100 Points)**
   - **Compliance & Certifications (50%)**: Validates mandatory environmental and governance certificates (ISO 14001, ISO 9001, OHSAS).
   - **Logistics Fulfillment (30%)**: Seamlessly calculates vendor score based on native Odoo On-Time Delivery rates.
   - **Carbon Footprint Proximity (20%)**: Geolocation distance calculation rewarding local vendors (<100 km) to curb freight emissions.
   - **Survey Audit Bonus**: Extra score boost for passing the annual corporate ESG survey.

2. **Smart PO Risk Intercept (Active Guardrail)**
   - Proactively intercepts and blocks confirmation of Purchase Orders issued to non-compliant ("Red") suppliers.
   - Displays clear warning dialogs listing the exact expired or missing certificates.

3. **Manager Override & Audit Trail**
   - Authorized procurement managers can toggle **Force / Override Compliance** for operational emergencies.
   - Automatically logs approval rationale, manager identity, and timestamp into the chatter audit trail.

4. **Automated Audit Scheduling**
   - Integrated with Odoo Survey.
   - Automatically emails periodic ESG questionnaires to active suppliers and imports scores directly back to partner cards.

5. **Visual Indicators & Badges**
   - Color-coded compliance ribbons on vendor cards, Kanban badges, and detailed score breakdown tables.

---

## 📋 Technical Requirements & Dependencies

- **Odoo Version**: 18.0 (Community or Enterprise)
- **Dependencies**:
  - `base`
  - `purchase`
  - `purchase_stock`
  - `survey`

---

## 🚀 Installation

1. Clone or download this repository.
2. Copy the `purchase_vendor_esg` directory into your Odoo `custom_addons` path.
3. Restart your Odoo server.
4. Enable **Developer Mode** in Settings.
5. Navigate to **Apps** &rarr; **Update Apps List**.
6. Search for `Vendor ESG & Sustainability Scorecard` and click **Activate**.

---

## ⚙️ Configuration

1. Go to **Purchase** &rarr; **Configuration** &rarr; **Settings** to enable or customize the global ESG blocking threshold.
2. Define mandatory certificates under **Purchase** &rarr; **Configuration** &rarr; **ESG Certificate Types** (e.g. ISO 14001).
3. Assign certificate attachments and valid expiration dates on the **Vendor** form under the new **ESG & Sustainability** tab.

---

## 💼 Explore Flagship Enterprise Suites by XodetiStudio

| Suite | Description | Pricing |
| :--- | :--- | :--- |
| **[Docu eSign Suite](https://xodetistudio.id/?deck=esign)** | PAdES-B-LT Cryptographic PDF Signing, Statutory PERURI e-Materai (UU No. 10/2020), Drag-and-Drop Coordinate Designer, Smart PIN 2FA. Zero SaaS tolls. | €600 (One-Time) |
| **[PathSFA Suite](https://xodetistudio.id)** | Enterprise Offline-First Sales Force Automation Flutter Mobile App + Odoo 18 Backend: GPS visit tracking, order booking, stock check, anti-fraud telemetry. | €2,999 (One-Time) |
| **[PathTMS Suite](https://xodetistudio.id)** | Enterprise Fleet, Dispatch & Transport Management System: delivery optimization, driver companion mobile app, fuel accounting, digital POD. | €2,999 (One-Time) |

---

## 📞 Support, Customization & Consulting

Need custom ESG metrics, automated carbon accounting formulas, or supplier portal extensions?

- **Website**: [https://xodetistudio.id](https://xodetistudio.id)
- **WhatsApp**: [+62 878-9516-4590](https://wa.me/6287895164590?text=Halo%20XodetiStudio%2C%20saya%20tertarik%20konsultasi%20modul%20Purchase%20Vendor%20ESG.)
- **Email**: [info@xodetistudio.id](mailto:info@xodetistudio.id)

---

## 📄 License

This module is licensed under the **GNU Lesser General Public License v3.0 (LGPL-3)**.  
Copyright &copy; 2026 [XodetiStudio](https://xodetistudio.id). Engineered by Muhammad Thoriq.

