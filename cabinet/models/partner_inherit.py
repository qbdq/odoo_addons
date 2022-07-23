from odoo import api, fields, models


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(string='Company Type',
                                    selection=[('patient', 'Patient'), ('person', 'Individual'),
                                               ('company', 'Company')],
                                    compute='', inverse='_write_company_type', default='patient')

    @api.onchange('company_type')
    def onchange_company_type(self):
        self.is_company = (self.company_type in ('company', 'patient'))

    def _write_company_type(self):
        for partner in self:
            partner.is_company = partner.company_type in ('company', 'patient')

    dob = fields.Date(string="Date d'anniversaire", required=False, )
    age = fields.Integer(string="Âge", required=False, )
    cin = fields.Char(string="CIN", required=False, )

    # Test general information
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], string="Blood Type")
    rh = fields.Selection([('plus', '+'), ('moins', '-')], string="Rh")

    # Biometry
    gender = fields.Selection(string="Genre", selection=[('male', 'Mâle'), ('female', 'Femelle'), ], required=True,
                              default="male")
    height = fields.Char(string='Hauteur', default=0)
    weight = fields.Char(string='Poids', default=0)
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], string="Blood Type", default='A')
    rh = fields.Selection([('plus', '+'), ('moins', '-')], string="Rh", default='plus')

    diseases_ids = fields.One2many('partner.diseases', 'partner_id')
    medication_ids = fields.One2many('partner.medication', 'partner_id')
    files_ids = fields.One2many('partner.files', 'partner_id')

    #
    # # life style
    # smoking = fields.Boolean(string="Smokes")
    # smoking_number = fields.Integer(string="Cigarretes a day")
    # ex_smoker = fields.Boolean(string="Ex-smoker")
    # age_start_smoking = fields.Integer(string="Age started to smoke")
    # age_quit_smoking = fields.Integer(string="Age of quitting")

    # alcohol = fields.Boolean(string="Drinks Alcohol")
    # ex_alcohol = fields.Boolean(string="Ex alcoholic")
    # age_start_drinking = fields.Integer(string="Age started to drink")
    # age_quit_drinking = fields.Integer(string="Age quit drinking")
    #

    # Medication
    # medical_vaccination_ids = fields.One2many('medical.vaccination','medical_patient_vaccines_id')
    # medical_appointments_ids = fields.One2many('medical.appointment','patient_id',string='Appointments')

    @api.onchange('dob')
    def calcul_age(self):
        for rec in self:
            if rec.dob:
                today = fields.Date.today()
                rec.age = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
            else:
                rec.age = 0


class PartnerDiseases(models.Model):
    _name = "partner.diseases"

    partner_id = fields.Many2one('res.partner')

    diseases_id = fields.Many2one("diseases.diseases", string="Maladies", required=True, )

    status_of_the_disease = fields.Selection(
        [('chronic', 'Chronique'), ('quo', 'Quo'), ('healed', 'Guéri'), ('improving', 'Améliorer'),
         ('worsening', 'Détérioration')], 'Status', help="Statut de la maladie")

    is_active = fields.Boolean('Active')
    age = fields.Integer('Age', help="Âge au moment du diagnostic")
    disease_severity = fields.Selection([('mild', 'Bénin'), ('moderate', 'Modéré'), ('severe', 'Sévère')], 'Gravité')
    is_allergy = fields.Boolean('Allergique')
    pregnancy_warning = fields.Boolean('Avertissement de grossesse')
    # weeks_of_pregnancy = fields.Integer('pregnancy week', help="Contracted in pregnancy week #")
    is_on_treatment = fields.Boolean('Sur le traitement', help="Actuellement en traitement")
    treatment_description = fields.Char('Description du traitement')
    date_start_treatment = fields.Date('Début du traitement')
    date_stop_treatment = fields.Date('Fin de traitement')


class Diseases(models.Model):
    _name = 'diseases.diseases'
    _rec_name = 'name'

    name = fields.Char()


class PartnerMedication(models.Model):
    _name = "partner.medication"

    madication_id = fields.Many2one("medication.medication", string="Médicament", required=True, )
    quantity = fields.Integer(string="Quantité", required=False, default=1)
    partner_id = fields.Many2one("res.partner")


class Medication(models.Model):
    _name = 'medication.medication'
    rec_name = "name"

    name = fields.Char()


class DossierPatient(models.Model):
    _name = "partner.files"
    _rec_name = "description"

    description = fields.Char(string="Description", required=False, )
    payment_method = fields.Selection(string="Methode", selection=[('cheque', 'Chèque'), ('espece', 'Espece'),
                                                                   ('carte bancaire', 'Carte Bancaire')],
                                      required=False, )
    condition = fields.Selection(string="Condition",
                                 selection=[('mensuel', 'Mensuel'), ('chaque seance', 'Chaque seance'), ],
                                 required=False, )
    full_price = fields.Integer(string="Total payable", required=False, )
    remaining = fields.Integer(string="Restant", required=False, )
    status = fields.Selection(string="Status", selection=[('paid', 'Payé'), ('in progress', 'En cours'),
                                                          ('no payement', 'Impayé'), ], required=False, )

    partner_id = fields.Many2one("res.partner")
    appointment_id = fields.Many2one('calendar.event', string='Rendez-vous', required=True)
    start_date = fields.Datetime(related="appointment_id.start", required=False, )

    type = fields.Selection(string="Type", selection=[('consultation', 'Consultation'), ('control', 'Contrôle'), ],
                            required=False, default='consultation')
