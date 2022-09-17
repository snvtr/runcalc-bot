import os

TOKEN = os.environ['VDOTBOT_TOKEN']

MESSAGES = {
          'help':  'I am able to understand:\n' + \
                   '/vdot [distance] [result] - VDOT from a race result\n' + \
                   '/race [VDOT] - projected race results based on VDOT\n' + \
                   '/agegraded [distance] [result] [age] [gender] - shows age graded percentage against the best result for this age\n' + \
                   '/agedist [age graded percentage] [age] [gender] - shows age graded results for a given age graded percentage\n' + \
                   '/coopert [time] - Cooper VO2max from a 1.5 mile result\n' + \
                   '/cooperd [distance] - Cooper VO2max from distance covered in 12 minutes\n' + \
                   '/balke [distance] - Balke VO2max from distance covered in 15 minutes\n'
                   '/helpdist - shows allowed distance formats\n' + \
                   '/helptime - shows allowed time formats\n' + \
                   '/helpvdot - shows allowed VDOT formats\n' + \
                   '/helpage - shows allowed age format\n' + \
                   '/helppercentage - shows allowed age graded percentage format\n' + \
                   '/helpgender - shows allowed gender formats',

           'helpvdot': 'VDOT should be entered as follows:\n' + \
                       'XX or XX.Y(Y) or XX,Y(Y) where Y(Y) is the decimal part. ' + \
                       'The decimal part is always rounded to 2 digits\n',

           'helptime': 'Time should be entered as follows:\n' + \
                       'HH:MM:SS or MM:SS, where HH is hours in 24H format, MM is minutes, SS is seconds.\n' + \
                       'Milliseconds are not ignored.',

           'helpdist': 'Distance should be entered as follows:\n' + \
                       '800 or 800m for 800 metres\n' + \
                       '1000 or 1000m or 1k for 1000 metres\n' + \
                       '1500 or 1500m or 1.5k for 1500 metres\n' + \
                       '1609 or 1609m or 1mile for 1 mile\n' + \
                       '2000 or 2000m or 2k for 2000m\n' + \
                       '2414 or 2414m or 1.5mile for 1.5 miles\n' + \
                       '3000 or 3000m or 3k for 3000 metres\n' + \
                       '4828 or 4828m or 3mile for 3 miles\n' + \
                       '5000 or 5000m or 5k for 5000 metres/5 Km\n' + \
                       '8000 or 8000m or 8k for 8 Km\n' + \
                       '8046 or 8046m or 5mile for 5 miles\n' + \
                       '10000 or 10000m or 10k for 10000 metres/10 Km\n' + \
                       '12000 or 12000m or 12k for 12 Km\n' + \
                       '15000 or 15000m or 15k for 15 Km\n' + \
                       '20000 or 20000m or 20k for 20 Km\n' + \
                       '21097 or 21097m or 21k or HM for Half-marathon\n' + \
                       '30000 or 30000m or 30k for 30 Km\n' + \
                       '42195 or 42195m or 42k or M for Marathon\n',
                       # + \
                       #'arbitrary distances are accepted in the range between '
                       # + \
                       #'800 and 42195 metres as XXXXX or XXXXXm (not implemented yet)' 

           'helpage':  'Age should be entered as follows:\n' + \
                       'an integer number between 5 and 99.\n',

           'helppercentage': 'Age percentage should be entered as follows:\n' + \
                             'an integer number between 0 and 100 with or without percent sign (%).\n',

           'helpgender': 'allowed gender values are M/m for males, F/f for females'

            }

DISTANCES = {          # the zero element carries the name:
            '800':     ['800 m', '800', '800m'],
            '1000':    ['1000 m', '1000', '1000m', '1k'],
            '1500':    ['1500 m', '1500', '1500m', '1.5k'],
            '1609.34': ['1 Mile', '1609', '1609m', '1mile', '1mi'],
            '2000':    ['2000 m', '2000', '2000m', '2k'],
            '2414.02': ['1.5 Miles', '2414', '2414m', '1.5mile', '1.5mi'],
            '3000':    ['3000 m', '3000', '3000m', '3k'],
            '3218.69': ['2 Miles', '3218', '3218m', '2mile', '2mi'],
            '4828.03': ['3 Miles', '4828', '4828m', '3mile', '3mi'],
            '5000':    ['5 Km', '5000', '5000m', '5k'],
            '8000':    ['8 Km', '8000', '8000m', '8k'],
            '8046.72': ['5 Miles', '8046', '8046m', '5mile', '5mi'],
            '10000':   ['10 Km', '10000', '10000m', '10k'],
            '12000':   ['12 Km', '12000', '12000m', '12k'],
            '15000':   ['15 Km', '15000', '15000m', '15k'],
            '20000':   ['20 Km', '20000', '20000m', '20k'],
            '21097':   ['Half-marathon', '21097', '21097m', '21k', 'hm'],
            '30000':   ['30 Km', '30000', '30000m', '30k'],
            '42195':   ['Marathon', '42195' ,'42195m', '42k', 'm']
            }

grade_files = [
             'AgeGrade.1609',
             'AgeGrade.5000',
             'AgeGrade.8000',
             'AgeGrade.10000',
             'AgeGrade.12000',
             'AgeGrade.15000',
             'AgeGrade.20000',
             'AgeGrade.21097',
             'AgeGrade.30000',
             'AgeGrade.42195'
             ]

grades  = {}
records = {}
