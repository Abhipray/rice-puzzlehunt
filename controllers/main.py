"""
Main page controller.
"""

__author__ = 'Abhipray Sahoo <abhiprays@gmail.com>'

import pages
import webapp2
from authentication import auth

PAGE_URI = '/main'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.get_logged_in_user()
        navbar = {}
        if user:
            navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score,
                'home':True
            }
        view = pages.render_view(PAGE_URI)
        pages.render_page(self, view, navbar)


class RulesHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.get_logged_in_user()
        navbar = {}
        if user:
            navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score,
                'rules' :True
            }
        view = pages.render_view('/rules')
        pages.render_page(self, view, navbar)


class FAQHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.get_logged_in_user()
        navbar = {}
        if user:
            navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score,
                'faq' : True
            }
        view = pages.render_view('/FAQ')
        pages.render_page(self, view, navbar)