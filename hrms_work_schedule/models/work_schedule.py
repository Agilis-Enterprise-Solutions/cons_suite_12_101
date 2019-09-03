# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    utc_offset = fields.Float(string="UTC Value", default=8.0)
    grace_period = fields.Float(string="Grace Period", default=0.25)
    break_time_hours = fields.Float(string="Breaktime", default=1.0)
    restday_workhours = fields.Float(string="Restday Work Hours", default=8.0,
                                     help="This will be the basis of computing Overtime Hours on the Restday or Holiday Works")

    @api.model
    def default_get(self, fields):
        res = super(ResourceCalendar, self).default_get(fields)
        res['tz'] = 'Asia/Manila'
        return res
