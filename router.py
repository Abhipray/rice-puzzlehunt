"""
Module for routing web requests to the correct controllers.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import webapp2
from controllers import main, apuzzle, allpuzzles, leaderboard


app = webapp2.WSGIApplication([
    ('/puzzle', apuzzle.APuzzleHandler),
    ('/allpuzzles', allpuzzles.AllPuzzlesHandler),
    ('/leaderboard', leaderboard.LeaderboardHandler),
    ('/rules', main.RulesHandler),
    ('/FAQ', main.FAQHandler),
    ('/.*', main.MainHandler)
], debug=True)