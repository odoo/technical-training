# -*- coding: utf-8 -*-
from odoo import http


class Academy(http.Controller):
    @http.route('/academy/course/', auth='public', website=True)
    def course(self, **kw):
        courses = http.request.env['openacademy.course'].search([])
        return http.request.render('openacademy.course', {
            'courses': courses,
        })

    @http.route('/academy/session_list/', auth='public', website=True)
    def session_list(self, **kw):
        sessions = http.request.env['openacademy.session'].search([])
        return http.request.render('openacademy.session_list', {
            'session': sessions
        })

    @http.route('/academy/<int:id>/', auth='public', website=True)
    def teacher(self, id):
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

    @http.route('/academy/<model("openacademy.session"):session>/', auth='public', website=True)
    def session(self, session):
        return http.request.render('openacademy.session', {
            'session': session
        })
