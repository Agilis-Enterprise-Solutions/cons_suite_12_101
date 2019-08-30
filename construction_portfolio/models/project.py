'''
Created on 11 August 2019

@author: Dennis
'''
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    parent_id = fields.Many2one("project.project", string="Portfolio", domain="[('project_type', 'in', ['porfolio'])]")
    project_count = fields.Integer(string="Projects", compute="_compute_project_count")

    @api.onchange('parent_id', 'name')
    def _onchange_portfolio(self):
        # data = self.search([('project_type', 'in', ['porfolio'])])
        # raise ValidationError(_('Data: %s'%(str(data))))
        for i in self:
            if i.parent_id:
                i.user_id = i.parent_id.user_id.id
                i.partner_id = i.parent_id.partner_id.id

    def _compute_project_count(self):
        for record in self:
            record.project_count = self.env['project.project'].search_count([('project_type','=','project'),('parent_id','=',record.id)])

    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        if not res.project_type in ['portfolio', False]:
            res.analytic_account_id.write({'parent_id':res.parent_id and res.parent_id.analytic_account_id.id or False})
        return res

    @api.multi
    def write(self, vals):
        res = super(Project, self).write(vals)
        self.analytic_account_id.write({'parent_id': self.parent_id and self.parent_id.analytic_account_id.id or False})
        return res
