'''
Created on 23 July 2019

@author: Dennis
'''
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class AccountAnalyticLine(models.Model):
    _inherit  = "account.analytic.line"


    @api.depends('account_id')
    def _get_project_value(self):
        for i in self:
            project = i.env['project.project'].search([('analytic_account_id','=', i.account_id.id)], limit=1)
            if project[:1]:
                i.project_id = project.id

    @api.depends('amount')
    def _get_analytic_type(self):
        for i in self:
            i.abs_amount = abs(i.amount)
            if i.amount <= 0.0:
                i.analytic_type = 'Expense'
            else:
                i.analytic_type = 'Income'

    analytic_type = fields.Selection([('Income', 'Income'), ('Expense', 'Expense')], string="Type", store=True, compute='_get_analytic_type')
    abs_amount = fields.Monetary(string="Absolute Amount", store=True, compute='_get_analytic_type')
    project_id = fields.Many2one('project.project', store=True, compute="_get_project_value")
    phase_id = fields.Many2one('project.phase', string="Phase")
    task_id = fields.Many2one('project.task', string="Task")
    project_boq_category = fields.Selection([
                                        ('meterial', 'Material'),
                                        ('subcon', 'Subcontractor'),
                                        ('labor', 'Human Resource/Labor'),
                                        ('equipment', 'Equipment'),
                                        ('overhead', 'Overhead'),
                                        ('other', 'Other')], string="Category")
