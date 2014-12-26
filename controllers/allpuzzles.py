"""
Allpuzzles page controller.
"""

__author__ = 'Abhipray Sahoo <abhiprays@gmail.com>'

import json
import logging
import pages
import webapp2
import models.users_db
import models.puzzle_data

from authentication import auth
from models.user import delete_user

PAGE_URI = '/allpuzzles'
MAX_ATTEMPTS = 5
PUZZLES_LIST = models.puzzle_data.puzzle_titles

class AllPuzzlesHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        if user.net_id in models.users_db.all_users:
            if user.team_name == None:
                #Initialize
                user.team_name = models.users_db.all_users[user.net_id]
                user.team_score = 0
                user.put()
            view = pages.render_view(PAGE_URI, {'puzzles': PUZZLES_LIST})
            navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score,
                'puzzles' : True
            }
            pages.render_page(self, view, navbar)
        else:
            delete_user(user)
            view = pages.render_view('/notsignedup', {})
            pages.render_page(self, view, {})



