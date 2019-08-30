# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"
    _description = "Project Inherited"


    # START Added SKIT
    boq_count = fields.Integer(compute='_compute_boq_count', string="BOQ")


    def _compute_boq_count(self):
        boq_data = self.env['project.boq'].read_group([
            ('project_id', 'in', self.ids)], ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in boq_data)
        for project in self:
            project.update({'boq_count': result.get(project.id, 0)})
    # END
