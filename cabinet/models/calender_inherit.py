from odoo import api, fields, models


class CalenderEventInherit(models.Model):
    _inherit = "calendar.event"

    type = fields.Selection(string="Type", selection=[('consultation', 'Consultation'), ('control', 'Contrôle'), ],
                            required=True, default='consultation')

    appointments_id = fields.Many2one('partner.files', string='Rendez-vous')
    patient_id = fields.Many2one("res.partner", string="Patient", required=False, )
    num_dossier = fields.Char(related="patient_id.num_dossier", required=False, )

    partner_ids = fields.Many2many(
        'res.partner', 'calendar_event_res_partner_rel',
        string='Attendees', )

    @api.onchange('patient_id')
    def set_partner_ids(self):
        for rec in self:
            if rec.patient_id not in rec.partner_ids:
                rec.partner_ids = rec.patient_id

    @api.model
    def create(self, values):
        res = super(CalenderEventInherit, self).create(values)
        try:
            file_val = {
                'appointment_id': res.id,
                'type': values.get('type'),
                'description': values.get('description'),
                'start_date': values.get('start'),
                'partner_id': values.get('patient_id'),
            }
            self.env['partner.files'].create(file_val)
        except:
            pass
        return res

    @api.onchange('type', 'patient_id')
    def change_name_field(self):
        for rec in self:
            if rec.type and rec.patient_id:
                rec.name = ""
                rec.name = f"{rec.type} - {rec.patient_id.name}"

    r_sph = fields.Float(string="SPH",  required=False, )
    r_cyl = fields.Float(string="CYL",  required=False, )
    r_axis = fields.Float(string="AXIS",  required=False, )
    r_av = fields.Float(string="AV",  required=False, )
    r_pup_dist = fields.Float(string="PUP DIST",  required=False, )
    r_add = fields.Float(string="ADD",  required=False, )
    r_prism = fields.Float(string="PRISM",  required=False, )
    r_base = fields.Float(string="BASE",  required=False, )

    g_sph = fields.Float(string="SPH",  required=False, )
    g_cyl = fields.Float(string="CYL",  required=False, )
    g_axis = fields.Float(string="AXIS",  required=False, )
    g_av = fields.Float(string="AV",  required=False, )
    g_pup_dist = fields.Float(string="PUP DIST",  required=False, )
    g_add = fields.Float(string="ADD",  required=False, )
    g_prism = fields.Float(string="PRISM",  required=False, )
    g_base = fields.Float(string="BASE",  required=False, )
