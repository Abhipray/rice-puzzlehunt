"""
Puzzle response page controller.
"""

__author__ = 'Abhipray Sahoo <abhiprays@gmail.com>'

import json
import logging
import pages
import webapp2
import models.puzzle_data


from authentication import auth
from datetime import datetime, timedelta
from models.attempt import get_attempts, create_attempt


# import models.sticky


PAGE_URI = '/apuzzle'
MAX_ATTEMPTS = 5
NUM_PUZZLES = len(models.puzzle_data.puzzle_titles)
CLOSING_TIME = models.puzzle_data.closing_time

class APuzzleHandler(webapp2.RequestHandler):

    def display_not_found(self, user):
        view = pages.render_view('/404', {})
        navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score
        }
        pages.render_page(self, view, navbar)

    def get(self):
        user = auth.require_login(self)
        puzzleNum = self.request.get('p')
        logging.info(puzzleNum)
        if puzzleNum == '':
            self.display_not_found(user)
        else:
            puzzleNum = int(puzzleNum)
            if puzzleNum > NUM_PUZZLES or puzzleNum < 1:
                self.display_not_found(user)
                return
            attempts = get_attempts(user, puzzleNum-1)
            logging.info(attempts)

            for a in attempts:
                a['time_added'] = (a['time_added'] - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')

            view = pages.render_view(PAGE_URI, {'attempts': attempts,
                                                'puzzleNum': puzzleNum,
                                                'puzzleTitle': models.puzzle_data.puzzle_titles[puzzleNum - 1]})
            navbar = {
                'team_name': user.team_name,
                'logged_in' : True,
                'team_score' : user.team_score
            }

            now = datetime.now() - timedelta(hours=6) #Get CST from UTC
            if now >= CLOSING_TIME:
                view = pages.render_view('/outoftime_main', {})
                pages.render_page(self, view, navbar)
                return
            pages.render_page(self, view, navbar)

    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return      # Should return error message here

        #Add a new attempt

        # Create attempt
        data = json.loads(self.request.get('data'))
        logging.info('Attempt Post: %s', data)
        puzzle_index = int(data['puzzleNum']) - 1
        now = datetime.now() - timedelta(hours=6) #Get CST from UTC
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        data['id'] = now
        attempts = get_attempts(user, puzzle_index)
        if len(attempts) == MAX_ATTEMPTS:
            data['success'] = False
            if data['attempt'] in models.puzzle_data.puzzle_answers[puzzle_index]:
                data['correctness'] = True
            else:
                data['correctness'] = False
            self.response.out.write(json.dumps(data))
            return

        #Check if already solved
        for a in attempts:
            if a['correctness']:
                #Solved so say it is
                data['success'] = False
                data['correctness'] = True
                self.response.out.write(json.dumps(data))
                return

        if data['attempt'].upper() in models.puzzle_data.puzzle_answers[puzzle_index]:
            data['correctness'] = True
            #Add up the score!
            user.team_score += 100 - len(attempts) * 10
            user.put()
            data['team_name'] = user.team_name
            data['team_score'] = user.team_score
        else:
            data['correctness'] = False
        #Save user results

        #Save the attempt
        attempt ={
            'puzzle_num': puzzle_index,
            'attempt_str': data['attempt'],
            'correctness': data['correctness']
        }
        create_attempt(user, attempt)

        # Respond

        data['success'] = True
        logging.info(data)
        self.response.out.write(json.dumps(data))


# class GarbageHandler(webapp2.RequestHandler):
#     def post(self):
#         # Authenticate user
#         user = auth.get_logged_in_user()
#         if not user:
#             return      # Should return error message here
#
#         sticky_id = self.request.get('id')
#         sticky = models.sticky.get_sticky(sticky_id)
#
#         # Make sure the user is not trying to delete someone else's sticky
#         assert sticky.user.key() == user.key()
#
#         models.sticky.delete_sticky(sticky)
#         self.response.out.write('Success!')