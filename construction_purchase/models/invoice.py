'''
Created on 02 August 2019

@author: Dennis
'''
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    project_related = fields.Boolean(string="A PO Project Related Invoice?", default=True, readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def _prepare_invoice_line_from_po_line(self, line):
        data = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        if self.project_related:
            data['phase_id'] = line.phase_id.id
            data['task_id'] = line.task_id.id
            data['project_boq_category'] = line.project_boq_category
            return data

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'


    phase_id = fields.Many2one('project.phase', string="Phase", domain="[('project_id.analytic_account_id', '=', account_analytic_id)]")
    task_id = fields.Many2one('project.task', string="Task", domain="[('phase_id', '=', phase_id)]")
    project_boq_category = fields.Selection([
                                        ('meterial', 'Material'),
                                        ('subcon', 'Subcontractor'),
                                        ('labor', 'Human Resource/Labor'),
                                        ('equipment', 'Equipment'),
                                        ('overhead', 'Overheads')], string="Category")
    recorded_analytic = fields.Boolean()

    # @api.constrains('task_id', 'project_boq_category')
    # def _check_data(self):
    #     for i in self:
    #         if not i.task_id and not i.project_boq_category in [False, 'overhead']:
    #             raise ValidationError(_('Please select related Task to those lines where "Category" in not equal to "Overheads" or Epmty'))

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def _prepare_analytic_line(self):
        data = super(AccountMoveLine, self)._prepare_analytic_line()
        for i in self.invoice_id.invoice_line_ids:
            if not i.recorded_analytic and self.name == i.name and self.analytic_account_id.id == i.account_analytic_id.id:# and self.unit_amount == i.quantity and self.general_account_id.id == i.account_id.id:
                data[0]['phase_id'] = i.phase_id.id
                data[0]['task_id'] = i.task_id.id
                data[0]['project_boq_category'] = i.project_boq_category
                i.write({'recorded_analytic': True})
                continue
        return data
