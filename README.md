rice-puzzlehunt
=============

Google App Engine webapp for the PuzzleHunt competition at Rice Unviersity sponsored by Microsoft. Web app uses CAS authentication for login, takes in string responses for puzzles and displays a leaderboard. 

Based on rice-stickies by Waseem Ahmad (WaseemTheDream/rice-stickies)
(http://www.waseemahmad.com/)

### Adding the users database

Assuming you have a list of users pre-registere, create `users_db.py` in the `models` directory with all `all_users` dictionary. Example `users_db.py`:

```python
# -*- coding: utf-8 -*-

team_names = u"""AMALFI 4417
Hunters
YOLO
fury
"""

user_netids = u"""ds11
sfdsz16
sfd2w33
zac22
"""

all_users = dict(zip(user_netids.split('\n'), team_names.split('\n')))

#Manually add administrators
all_users['as83'] = u'A-Team 1'
all_users['as110'] = u'iWin'
all_users['sjk3'] = u"A-Team 2"

```

### Adding the puzzles

To add the puzzle names and correct responses to each, create `puzzle_data.py` in the `models` directory with two lists, `puzzle_titles` and `puzzle_answers` as follows:

```python
puzzle_titles = [
    'The IEEE Shirt Mystery',
    'The IEEE Shirt Mystery 2'
]

#Add all possible answers (upper-case) in a tuple
puzzle_answers = [
                 ('FLOPPYDISK2', 'FLOPPYY', 'FLOPS'),
                 ('DUMMY',)
]

```

### Competition time settings

Two variables hide parts of the app after the specified times-- `closing_time` and `leaderboard_hide_time`. `leaderboard_time` sets the time after which leaderboard is hidden from users. `closing_time` makes the leaderboard visibile and shuts off the puzzle pages that take user responses; it marks the end of the competition. 

Set the two variables in `puzzle_data.py` as follows:

```python
from datetime import datetime

closing_time = datetime(2014, 11, 15, 16, 15, 0, 0) #Close at 4:15pm

leaderboard_hide_time = datetime(2014, 11, 15, 15, 45, 0, 0) #Hide at 3:45pm
```

