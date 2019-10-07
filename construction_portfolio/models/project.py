'''
Created on 11 August 2019

@author: Dennis
'''
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    @api.onchange('parent_id', 'project_type')
    def _onchange_portfolio(self):
        if self.project_type == 'project' and self.parent_id:
            self.user_id = self.parent_id.user_id and self.parent_id.user_id.id or False
            self.partner_id = self.parent_id.partner_id and self.parent_id.partner_id.id or False

    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        if res.project_type == 'porfolio':
            if res.analytic_account_id:
                res.analytic_account_id.write({
                    'group_id': self.env['account.analytic.group'].create({'name': res.name, 'description': 'Project Portfolio'}).id
                })
        elif res.project_type == 'project' and res.parent_id:
            if res.analytic_account_id and res.parent_id.analytic_account_id and res.parent_id.analytic_account_id.group_id:
                res.analytic_account_id.write({
                    'group_id': res.parent_id.analytic_account_id.group_id.id
                })
        return res

    @api.multi
    def write(self, vals):
        res = super(Project, self).write(vals)
        if res.project_type == 'porfolio':
            if res.analytic_account_id and not res.analytic_account_id.group_id:
                res.analytic_account_id.write({
                    'group_id': self.env['account.analytic.group'].create({'name': res.name, 'description': 'Project Portfolio'}).id
                })
        elif res.project_type == 'project' and not res.parent_id:
            if res.analytic_account_id:
                res.analytic_account_id.write({
                    'group_id': False
                })
        return res
