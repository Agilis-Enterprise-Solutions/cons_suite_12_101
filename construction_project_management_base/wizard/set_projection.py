'''
Created on 4 July 2019

@author: Dennis
'''
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class SetProjection(models.TransientModel):
    _name = 'set.projection'

    survey_frequent = fields.Selection([('week', 'Week'), ('month', 'Month'), ('quarter', 'Quarter')], string="Frequent Status Review", default="month")
    number_of_frequent = fields.Integer(string="Frequent Duration", default="1", help="Number of Weeks/Months/Quarters")
    start_date = string = fields.Date(string="Start Date")

    @api.multi
    def set_projection(self):
        for i in self:
            start_date = i.start_date#datetime.strptime(i.start_date, DF)
            data_record = []
            if i.survey_frequent == 'week':
                for r in range(i.number_of_frequent):
                    self.env['project.projection.accomplishment'].create({
                        'project_id': self._context.get('active_id'),
                        'date': (start_date + relativedelta(days=7)).strftime(DF)
                    })
                    start_date = start_date + relativedelta(days=7)
            else:
                months = 1
                if i.survey_frequent == 'quarter': months = 4
                for r in range(i.number_of_frequent):
                    self.env['project.projection.accomplishment'].create({
                        'project_id': self._context.get('active_id'),
                        'date': (start_date + relativedelta(months=months)).strftime(DF)
                    })
                    start_date = start_date + relativedelta(months=months)
            # project = self.env['project.project'].browse(self._context.get('active_id'))
            # project.write({'projection_set': True})
