"""
Leaderboard page controller.
"""

__author__ = 'Abhipray Sahoo <abhiprays@gmail.com>'

import pages
import webapp2
from models.user import get_users_leaderboard
from authentication import auth
from datetime import datetime, timedelta
import models.puzzle_data

PAGE_URI = '/leaderboard'
HIDE_TIME = models.puzzle_data.leaderboard_hide_time
CLOSE_TIME = models.puzzle_data.closing_time

class LeaderboardHandler(webapp2.RequestHandler):
    def get(self):
        # if now
        #See if user if logged in
        user = auth.get_logged_in_user()
        navbar = {}
        if user:
            navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score
            }
        now = datetime.now() - timedelta(hours=6) #Get CST from UTC

        if now > HIDE_TIME and now < CLOSE_TIME:
            view = pages.render_view('/outoftime', {})
            pages.render_page(self, view, navbar)
            return

        scores = get_users_leaderboard()
        view = pages.render_view(PAGE_URI, {'teams': scores})
        pages.render_page(self, view, navbar)