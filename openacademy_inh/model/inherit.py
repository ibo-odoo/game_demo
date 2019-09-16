from odoo import fields,models,api
class Inheritance(models.Model):
    _inherit ='openacademy.course' 

    idea_ids = fields.Integer(String="No of ids")
