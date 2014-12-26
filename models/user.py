"""
Model definition and functions for users.
"""

__author__ = 'Abhipray Sahoo <abhiprays@gmail.com>'

from google.appengine.ext import db

NUM_PUZZLES = 13 #Max number of puzzles


class User(db.Model):
    net_id = db.StringProperty(required=True)
    team_name = db.StringProperty(required=False)
    team_score = db.IntegerProperty(indexed=True)

    def to_json(self):
        return {
            'net_id': self.net_id,
            'team_name': self.team_name,
            'team_score':self.team_score
        }

def get_user(net_id, create=False):
    user = User.gql('WHERE net_id=:1', net_id).get()
    if not user and create:
        user = User(net_id=net_id)
        user.put()
    return user


def get_users_leaderboard():
    return [user.to_json() for user in User.gql('ORDER BY team_score DESC')]

def delete_user(user):
    user.delete()