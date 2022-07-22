from odoo import api, fields, models


class CalenderEventInherit(models.Model):
    _inherit = "calendar.event"

    type = fields.Selection(string="Type", selection=[('Consultation', 'Consultation'), ('Control', 'Control'), ],
                            required=True, default='Consultation')

    appointments_id = fields.Many2one('partner.files', string='File name')

    @api.onchange('type')
    def change_name_field(self):
        for rec in self:
            if rec.type:
                rec.name = ""
                rec.name = f"{rec.type} - {rec.partner_ids.name}"
