from odoo import models, fields,api

class Busdemo(models.Model):
    _name = 'bus.demo'

    name = fields.Char(string="Title", required=True)
    image = fields.Binary()

# For sending notification
    @api.model
    def notify_student(self,notification):
        notifications = []
        print(notification)
        students = self.env['busdemo.student'].search([])
        for user in students:
            notif = notification
            notifications.append([(self._cr.dbname, 'image.data', user.partner_id.id), notif])
        print(notifications)
        if len(notifications) > 0:
            self.env['bus.bus'].sendmany(notifications)

class teadent(models.Model):
    _name = 'busdemo.student'

    partner_id = fields.Many2one('res.partner',string="Student List")

    @api.model
    def add_member(self, partner_id):
        print(partner_id)
        student  = self.search([('partner_id', '=', partner_id)])
        print(student)
        if not student:
            student = self.create({
                'partner_id': partner_id
            })
        return student

