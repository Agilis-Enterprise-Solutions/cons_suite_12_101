# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    nightdiff_hour_start = fields.Float(string="Time Start", default=22.00)
    nightdiff_hour_end = fields.Float(string="Time End", default=06.00)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env.user.company_id.write({
            'nightdiff_hour_start': self.nightdiff_hour_start,
            'nightdiff_hour_end': self.nightdiff_hour_start})

    def _get_default_nightdiff_hour_start(self):
        nightdiff = self.env.user.company_id.nightdiff_hour_start
        return nightdiff

    def _get_default_nightdiff_hour_end(self):
        nightdiff = self.env.user.company_id.nightdiff_hour_end
        return nightdiff

    nightdiff_hour_start = fields.Float(string="Time Start", default=_get_default_nightdiff_hour_start)
    nightdiff_hour_end = fields.Float(string="Time End", default=_get_default_nightdiff_hour_end)

    minimum_overtime_file = fields.Float(string="Minimum Overtime")
    overtime_rounding = fields.Float(string="Overtime Rounding")
    regular_working_hours = fields.Boolean(string="Enforce  Regular Working Hours?",
                                         help=""""While verifing as rendered, The System should as well check if the employee has rendered the regular work hours mandated.
                                         Scenario:
                                         Actual Attendance: 08:30 to 21:00 (Late for 30 mins)
                                         Filled Overtime: 17:00 to 21:00
                                         To be able to Verify as Rendered, the user should Edit the timestart to 17:30""")
