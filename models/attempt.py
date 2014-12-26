__author__ = 'Abhipray'

from google.appengine.ext import db
from user import User


class Attempt(db.Model):
    user = db.ReferenceProperty(User,
                                required=True)
    time_added = db.DateTimeProperty(auto_now=True)
    attempt_str = db.StringProperty(required=True)
    puzzle_num = db.IntegerProperty(indexed=True)
    correctness = db.BooleanProperty(indexed=True)
    team_name = db.StringProperty(indexed=True)

    def to_json(self):
        return {
            'id': str(self.key()),
            'time_added': self.time_added,
            'puzzle_num': self.puzzle_num,
            'attempt_str': self.attempt_str,
            'correctness': self.correctness
        }


def create_attempt(user, attempt):
    attempt = Attempt(
        user=user.key(),
        team_name= user.team_name,
        # time_added=attempt['time_added'],
        puzzle_num=attempt['puzzle_num'],
        attempt_str=attempt['attempt_str'],
        correctness=attempt['correctness'])
    attempt.put()
    return attempt


def get_attempt(key):
    return Attempt.get(key)


def get_successes(user):
    return [attempt.to_json() for attempt in Attempt.gql('WHERE user=:1 AND correctness=:2', user,
                                                         True)]

def delete_attempt(attempt):
    # Refactored into this method incase there are other things to be done
    # before deleting a attempt
    attempt.delete()


def get_attempts(user, puzzle_num):
    return [attempt.to_json() for attempt in Attempt.gql('WHERE user=:1 AND puzzle_num=:2 ORDER BY time_added DESC', user, puzzle_num)]
