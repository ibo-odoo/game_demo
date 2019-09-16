# -*- coding: utf-8 -*

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request
from odoo import http

# For creating channel
class TeacherBusController(BusController):
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'image.data', request.env.user.partner_id.id))
        print("======> channels",channels)
        return super(TeacherBusController, self)._poll(dbname, channels, last, options)

    @http.route('/teacher/',type='json', auth='public')
    def _student(self,partner_id):
        # print(partner_id)
        enroll = request.env['busdemo.student'].sudo().add_member(partner_id)
        print(partner_id)
        return bool(enroll)
