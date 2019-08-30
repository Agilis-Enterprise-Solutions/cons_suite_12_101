# -*- coding: utf-8 -*-

'''
Created on 6 Aug 2019

@author: Srikesh Infotech
'''
from odoo import api, fields, models
from datetime import datetime


class ProjectVisualInspection(models.Model):
    _name = 'project.visual.inspection'
    _description = "Visual Inspection"
    _order = 'date desc'

    date = fields.Date(string='Date', required=True)
    description = fields.Text(string='Description', required=True)
    actual_accomplishment = fields.Float(string='Actual Accomplishment',
                                         required=True)
    task_id = fields.Many2one('project.task', 'Task')

    # @api.multi
    # @api.onchange('date', 'task_id')
    # def _check_unique_date(self):
    #     if not self.date:
    #         return
    #     rest_of_vals = self.task_id.visual_inspection - self
    #     for record in rest_of_vals:
    #         previous_date = record.date
    #         current_date = record.date
    #         p_date = self.trunc_datetime((previous_date))
    #         c_date = self.trunc_datetime((current_date))
    #         if p_date == c_date and record.task_id.id == self.task_id.id:
    #             return {
    #                  'warning': {'title': 'Error!', 'message': 'Actual Accomplishment should not be more than one time for same period.'},
    #                  'value': {
    #                              'date': None,
    #                         }
    #             }
    #
    # def trunc_datetime(self, date):
    #     return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    @api.multi
    def document_attach(self):
        """This method is to upload files in the
        visual inspection

        :rtype dict.

        :return returns the popup form to attach file

        """
        upload = self.env['project.document.attach'].search(
                         [('res_id', '=', self.id)])
        res_id = 0
        if upload:
            for line in upload:
                if line.res_id == self.id:
                    res_id = line.id
        ctx = dict(self._context, res_id=self.id)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.document.attach',
            'res_id': res_id,
            'res_name': "Attach File",
            'create': False,
            'target': 'new',
            'context': ctx
        }


class ProjectTask(models.Model):
    _inherit = 'project.task'

    actual_accomplishment = fields.Float(string="Actual Accomplishment",
                                         compute='update_actual_accomplishment')
    visual_inspection = fields.One2many(
        'project.visual.inspection', 'task_id', 'Visual Inspection',
        copy=True)

    @api.depends('visual_inspection.actual_accomplishment')
    def update_actual_accomplishment(self):
        for ids in self:
            accomplishment = ids.env['project.visual.inspection'].search([('task_id', '=', ids.id)], limit=1, order='date desc')
            ids.update({'actual_accomplishment': accomplishment[:1] and accomplishment.actual_accomplishment or 0.0})

        # actual_accomplishment = 0
        # maxdate = '0000-00-00'
        # for ids in self:
        #     #===================================================================
        #     # if ids.visual_inspection:
        #     #     visual_size = len(ids.visual_inspection) - 1
        #     #===================================================================
        #     vals = []
        #     for visual in ids.visual_inspection:
        #         maxdate = max(visual.date, maxdate)
        #         vals.append({'date': visual.date,
        #                      'id': visual.id,
        #                      'value': visual.actual_accomplishment})
        #         actual_accomplishment += visual.actual_accomplishment
        #     for val in vals:
        #         if val.get('date') == maxdate:
        #             ids.update({'actual_accomplishment': val.get('value')
        #                         })


class DocumentsAttach(models.Model):
    _name = 'project.document.attach'
    _description = "Attach documents for visual inspection"

    attachment_ids = fields.Many2many(
            'ir.attachment',
            string="Attachments",
            help="Attachments are linked to a document "
                 "through model / res_id"
    )
    res_id = fields.Integer('res_id')

    @api.multi
    def upload(self):

        """Save uploaded attachments

          :rtype: dict

          :return returns from saving

        """
        self.res_id = self.env.context['res_id']
        tasks = self.env['project.visual.inspection'].search(
                                 [('id', '=', self.res_id)])
        for line in tasks:
            line.attachment_ids = [(6, 0, self.attachment_ids.ids)]
