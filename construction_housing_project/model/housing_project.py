'''
Created on 4 July 2019

@author: Dennis
'''
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class HousingModel(models.Model):
    _name = 'housing.model'

    name = fields.Char(string="Model", required=True)
    description = fields.Char(string="Description")
    year_month = fields.Char(string="Year Month")

class HousingBlock(models.Model):
    _name = 'housing.block'

    name = fields.Char(string="Block", required=True)
    description = fields.Char(string="Description")

class HousingProjectModelImage(models.Model):
    _inherit = 'product.image'
    _description = 'House Model Image'

    housing_model_tmpl_id = fields.Many2one('housing.project.model', string='Related Models', copy=True)


class HousingProjectModel(models.Model):
    _name = 'housing.project.model'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin']

    @api.depends("house_model_id", "house_model_id.name", "block_id", "block_id.name", "lot_number")
    def _get_fullname(self):
        for i in self:
            if i.house_model_id and i.block_id and i.lot_number:
                i.name = "%s %s (%s)"%(i.lot_number, i.house_model_id.name, i.block_id.name)

    house_model_id = fields.Many2one('housing.model', string="House Model", required=True, track_visibility="always")
    block_id = fields.Many2one('housing.block', string="Block", required=True, track_visibility="always")
    lot_number = fields.Char(string="Lot No.", required=True, track_visibility="always")
    description = fields.Html(string="Description", track_visibility="always")
    name = fields.Char(string="Name", compute="_get_fullname", store=True)
    image = fields.Binary(string="Model Image", track_visibility="always")
    house_model_image_ids = fields.One2many('product.image', 'housing_model_tmpl_id', string='Images')
    # model_image_ids = fields.One2many('housing.project.mod, track_visibility="always"el.image', 'model_tmpl_id', string='Images')


    @api.constrains("name")
    def _check_name(self):
        for i in self:
            data_dup = self.search([('id', 'not in', [i.id]), ('name', '=', i.name)], limit=1)
            if data_dup[:1]:
                raise ValidationError(_("%s already profiled in the system"%(i.name)))
