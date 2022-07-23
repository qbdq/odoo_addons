from odoo import api, fields, models


class CalenderEventInherit(models.Model):
    _inherit = "calendar.event"

    type = fields.Selection(string="Type", selection=[('consultation', 'Consultation'), ('control', 'Control'), ],
                            required=True, default='consultation')

    appointments_id = fields.Many2one('partner.files', string='File name')
    patient_id = fields.Many2one("res.partner", string="Patient", required=False, )
    partner_ids = fields.Many2many(
        'res.partner', 'calendar_event_res_partner_rel',
        string='Attendees', )

    @api.onchange('patient_id')
    def set_partner_ids(self):
        for rec in self:
            if rec.patient_id not in rec.partner_ids:
                rec.partner_ids = rec.patient_id

    @api.model_create_multi
    def create(self, values):
        res = super(CalenderEventInherit, self).create(values)
        file_val = {
            'appointment_id': res.id,
            'type': values.get('type'),
            'description': values.get('description'),
            'start_date': values.get('start'),
            'partner_id': values.get('patient_id'),
        }
        self.env['partner.files'].create(file_val)

        return res

    @api.onchange('type')
    def change_name_field(self):
        for rec in self:
            if rec.type:
                rec.name = ""
                rec.name = f"{rec.type} - {rec.partner_ids.name}"
