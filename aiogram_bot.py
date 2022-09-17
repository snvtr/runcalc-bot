import logging
#import asyncio
#from types import NoneType

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
#from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode
from aiogram.utils.helper import Helper, HelperMode, ListItem

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config  import TOKEN, MESSAGES, DISTANCES
import math
from pprint import pprint

logging.basicConfig(format=u'%(filename)s [ln:%(lineno)+3s]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['vdot'])
async def process_start_command(message: types.Message):
    ''' returns VDOT from a race result '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 2:
        await message.reply('vdot(): not enough arguments')
        return
    dist = get_dst(arguments[0]) 
    res  = get_res(arguments[1])
    if dist is None or res is None:
        await message.reply('vdot(): badly formed arguments')
    else:
        await message.reply(build_dist_time(dist, res))

@dp.message_handler(commands=['race'])
async def process_start_command(message: types.Message):
    ''' returns probable race results from VDOT '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('race(): not enough arguments')
        return
    vdot = get_vdot(arguments[0].replace(',', '.'))
    if vdot is None or vdot > 99.99:
        await message.reply('race(): badly formed arguments')
    else:
        await message.reply(build_vdot(vdot))

@dp.message_handler(commands=['agegraded'])
async def process_start_command(message: types.Message):
    ''' returns age graded percentage of the best time for a given age '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 4:
        await message.reply('agegraded(): not enough arguments')
        return
    dist   = get_dst(arguments[0]) 
    res    = get_res(arguments[1])
    age    = get_age(arguments[2])
    gender = get_gender(arguments[3])
    if dist is None or res is None or age is None or gender is None:
        await message.reply('agegraded(): badly formed arguments')
    else:
        await message.reply(build_agegraded(dist, res, age, gender))

@dp.message_handler(commands=['agedist'])
async def process_start_command(message: types.Message):
    ''' returns age graded percentage of the best time for a given age '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 3:
        await message.reply('agedist(): not enough arguments')
        return
    percent = get_pct(arguments[0]) 
    age     = get_age(arguments[1])
    gender  = get_gender(arguments[2])
    if percent is None or age is None or gender is None:
        await message.reply('agedist(): badly formed arguments')
    else:
        await message.reply(build_agedist(percent, age, gender))

@dp.message_handler(commands=['coopert'])
async def process_start_command(message: types.Message):
    ''' returns cooper test result from time '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('coopert(): not enough arguments')
        return
    res = get_res(arguments[0])
    if res is not None:
        await message.reply(build_cooper_t(res))
    else:
        await message.reply('coopert(): badly formed arguments')

@dp.message_handler(commands=['cooperd'])
async def process_start_command(message: types.Message):
    ''' returns cooper test result from distance '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('cooperd(): not enough arguments')
        return
    try:
        dist = float(arguments[0])
    except:
        dist = None
    if dist is not None:
        await message.reply(build_cooper(dist))
    else:
        await message.reply('cooperd(): badly formed arguments')

@dp.message_handler(commands=['balke'])
async def process_start_command(message: types.Message):
    ''' returns cooper test result from distance '''
    argument = message.get_args()
    arguments = argument.rstrip().split(' ')
    if len(arguments) < 1:
        await message.reply('balke(): not enough arguments')
        return
    try:
        dist = float(arguments[0])
    except:
        dist = None
    if dist is not None:
        await message.reply(build_balke(dist))
    else:
        await message.reply('balke(): badly formed arguments')

@dp.message_handler(commands=['help', 'start'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])

@dp.message_handler(commands=['helptime'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helptime'])

@dp.message_handler(commands=['helpdist'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpdist'])

@dp.message_handler(commands=['helpvdot'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpvdot'])

@dp.message_handler(commands=['helpage'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpage'])

@dp.message_handler(commands=['helppercentage'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helppercentage'])

@dp.message_handler(commands=['helpgender'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['helpgender'])

@dp.message_handler()
async def echo_message(msg: types.Message):
    #await bot.send_message(msg.from_user.id, reply, parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(msg.from_user.id, 'not a valid message. run /help command', parse_mode=ParseMode.MARKDOWN)

def get_pace(dist, res):
    ''' 
    returns pace for a given dist/res without leading hours: Mi:SS/km 
    >>> get_pace(1000, 5)
    '05:00'
    >>> get_pace(20000, 80)
    '04:00'
    '''
    return time_to_str(res/(dist/1000))[3:]

def get_vdot(raw_vdot):
    ''' 
    checks if vdot value is valid 
    >>> get_vdot('54.321')
    54.32
    >>> get_vdot('54,321')
    54.32
    >>> get_vdot('xyz')
    
    '''
    try:
        vdot = round(float(raw_vdot), 2)
    except:
        vdot = None
    return vdot

def get_dst(raw_dst):
    '''
    checks if distance from a message is valid
    >>> get_dst('1000m') 
    '1000'
    >>> get_dst('12345K')

    '''
    for d in DISTANCES.keys():
        if raw_dst.lower() in DISTANCES[d]:
            return DISTANCES[d][1]
    return None

def get_dst_name(raw_dst):
    '''
    returns distance user-friendly name
    >>> get_dst('1000') 
    '1000 m'
    >>> get_dst('12345K')

    '''
    for d in DISTANCES.keys():
        if raw_dst.lower() in DISTANCES[d]:
            return DISTANCES[d][0]
    return None


def get_age(raw_age):
    '''
    checks if age is valid
    >>> get_age('99') 
    99
    >>> get_age('4')

    '''
    if int(raw_age) < 5 and int(raw_age) > 99:
        return None
    else:
        return int(raw_age)


def get_pct(raw_pct):
    '''
    checks if percentage is valid
    >>> get_pct('99%') 
    99
    >>> get_pct('123%')
    
    '''
    pct = raw_pct.replace('%', '')
    if int(pct) < 0 or int(pct) > 100:
        return None
    else:
        return int(pct)

def get_gender(raw_gender):
    '''
    checks if gender is valid
    >>> get_gender('%') 
    
    >>> get_gender('f')
    F 
    '''
    gender = raw_gender.upper()
    if gender not in ['F', 'M']:
        return None
    else:
        return gender

def get_res(raw_res):
    '''
    checks if result time from a message is valid
    >>> get_res('05:11')
    '00:05:11'
    >>> get_res('02:43:56')
    '02:43:56'
    >>> get_res('44:33:66')

    '''
    items = raw_res.strip().split(':')
    if len(items) < 2 or len(items) > 3:
        return None
    if len(items) == 3:
        if int(items[0]) > 23 or int(items[0]) < 0:
            return None
        if int(items[1]) > 59 or int(items[1]) < 0:
            return None
        if int(items[2]) > 59 or int(items[2]) < 0:
            return None
        return raw_res #int(items[0])*3600 + int(items[1])*60 + int(items[2])
    if len(items) == 2:
        if int(items[0]) > 59 or int(items[0]) < 0:
            return None
        if int(items[1]) > 59 or int(items[1]) < 0:
            return None
        return '00:'+raw_res #int(items[1])*60 + int(items[2])
    return None

def balke(distance):
    '''
    Balke 15 min running test
    >>> balke(3000)
    '44.82'
    >>> balke(6666)
    'distance out of range'
    >>> balke(99)
    'distance out of range'
    '''
    if (distance < 100):
        return 'distance out of range'
    if (distance > 6500):
        return 'distance out of range'
    vo2max = 0.172 * (distance / 15 - 133) + 33.3
    return '{:2.2f}'.format(vo2max)

def cooper(distance):
    '''
    cooper test from distance
    >>> cooper(2400)
    '42.37'
    >>> cooper(99)
    'distance out of range'
    >>> cooper(5555)
    'distance out of range'
    '''
    if (distance < 100):
        return 'distance out of range'
    if (distance > 5000):
        return 'distance out of range'
    vo2max = (distance - 504.9)/44.73
    return '{:2.2f}'.format(vo2max)

def cooper_from_time(str_time):
    '''
    cooper test from time
    >>> cooper_from_time('00:12:00')
    '43.75'
    >>> cooper_from_time('00:08:00')
    'time out of range'
    >>> cooper_from_time('00:31:24')
    'time out of range'
    '''
    time_t = str_to_time(str_time)
    if time_t < 9 or time_t > 30:
        return 'time out of range'
    return '{:2.2f}'.format((483 / time_t) + 3.5)

def cooper_from_time_indian(str_time):
    ''' cooper test from time, indian mod:
     - Get distance/time like for VDOT.
     - Convert it to Daniels VDOT with daniels().
     - Then with reverse() find time for 1.5 miles and put this time into the cooper formulas
    '''
    time_t = str_to_time(str_time)
    if time_t < 9 or time_t > 30:
        return 'time out of range'
    new_dist = 2400*12.0/time_t
    return cooper_indian_mod(new_dist)

def cooper_indian_mod(distance):
    ''' cooper test, indian improvement from distance '''
    if (distance < 100):
        return 'distance out of range'
    if (distance > 5000):
        return 'distance out of range'
    vo2max = 21.01*distance/1000 - 11.04
    return '{:2.2f}'.format(vo2max)

def daniels(distance, str_time):
    '''
    the main function, converts distance+time to VDOT
    >>> daniels(3000, '00:12:00')
    47.85
    '''
    duration = float(str_to_time(str_time))
    velocity = float(distance) / duration
    return round((-4.60 + 0.182258 * velocity + 0.000104 * math.pow(velocity,2)) / (0.8 + 0.1894393 * math.exp(-0.012778 * duration) + 0.2989558 * math.exp(-0.1932605 * duration)),2)

def get_function(race_d,race_t,race_VDOT):
    ''' a helper function for newton approximation '''
    upper = 0.000104 * race_d**2 * race_t**-2 + 0.182258 * race_d * race_t**-1 - 4.6
    lower = 0.2989558 * math.exp(-0.1932605*race_t) + 0.1894393 * math.exp(-0.012778*race_t) + 0.8
    return (upper/lower - float(race_VDOT))

def get_derivative(race_d,race_t,race_VDOT):
    ''' a helper function for newton approximation '''
    upper = ((((0.2989558*math.exp(-0.1932605*race_t))+(0.1894393*math.exp(-0.012778*race_t))+0.8)*((-0.000208)*(race_d**2)*(race_t**-3))-((0.182258)*race_d*(race_t**-2)))-(race_VDOT*((0.2989558)*(math.exp(-0.1932605*race_t))+(0.1894393)*(math.exp(-0.012778*race_t)))))
    lower = (0.2989558 * math.exp(-0.1932605 * race_t) + 0.1894393 * math.exp(-0.012778 * race_t) + 0.8)**2
    return (upper/lower)

def reverse(distance, VDOT):
    '''
    Reverse function for daniels(), gets time based on VDOT and distance.
    It approximates the output based on Newton approximation
    >>> reverse(5000, 30)
    30.68
    '''
    time = 60
    if distance <= 50000:
        time = 250
    if distance <= 42200:
        time = 220
    if distance <= 21100:
        time = 110
    if distance <= 10000:
        time = 50
    if distance <= 5000:
        time = 25
    if distance <= 3000:
        time = 12
    function   = get_function (float(distance), float(time), float(VDOT))
    derivative = get_derivative (float(distance), float(time), float(VDOT)) 
    i = 0
    while abs(function/derivative) > 0.000001:
        i = i + 1
        if i > 100:
            break
        time = time - function/derivative
        function   = get_function (float(distance), float(time), float(VDOT))
        derivative = get_derivative (float(distance), float(time), float(VDOT))
    return round(time, 2)

def time_to_str(time_t):
    '''
    >>> time_to_str(123.45)
    02:03:27
    '''
    hours = time_t // 60
    secs, mins  = math.modf(time_t - hours*60)
    secs = round(secs*60)
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))

def str_to_time(time_str):
    '''
    >>> str_to_time('02:03:27')
    123.45
    '''
    time_parts = time_str.split(':')
    return round(float(time_parts[0]) * 60 + float(time_parts[1]) + (float(time_parts[2]) / 60), 2)

def build_vdot(vdot):
    ''' formatted reply '''
    json_parts = []
    for d in DISTANCES.keys():
        dist = float(d)
        secs = reverse(dist, vdot)
        pace = get_pace(dist, secs)
        json_parts.append(DISTANCES[d][0]+': '+time_to_str(secs)+' ('+pace+'/km)')
    return '\n'.join(json_parts)

def build_dist_time(dist, dist_time):
    ''' formatted reply '''
    return 'VDOT: ' + str(daniels(dist, dist_time))

def build_cooper(distance):
    ''' formatted reply '''
    return ''.join(['VO2max (Cooper test based on distance): ',cooper(int(distance)),',\n','VO2max (Cooper Indian Mod): ',cooper_indian_mod(int(distance))])

def build_cooper_t(str_time):
    ''' formatted reply '''
    return ''.join(['VO2max (Cooper test based on time): ',cooper_from_time(str_time),',\n','VO2max (Cooper Indian Mod): ',cooper_from_time_indian(str_time)])

def build_balke(distance):
    ''' formatted reply '''
    return ''.join(['VO2max (Balke test based on distance): ',balke(int(distance)),])

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

def load_grade_files():
    '''
    inits all the dictionaries with grades
    '''
    for grade_file in grade_files:
        distance = get_dst(grade_file[9:])
        print('load_grade_files():', grade_file, distance)

        grades[distance] = {}
        grades[distance]['F'] = {}
        grades[distance]['M'] = {}
        records[distance] = {}
        with open('./AgeGrades/'+grade_file, 'r') as f:
            for ln in f:
                if ln.find(':') >= 0:
                    items = ln.rstrip().split('  ')
                    gender   = items[0][0]
                    record_t = items[1]
                    records[distance][gender] = record_t
                    continue
                gender = ln[0]
                age    = int(ln[2:4].rstrip())
                coeff  = float(ln[5:])
                grades[distance][gender][age] = coeff
    for key in records.keys():
        print('load_grade_files():', key)                


def get_dist_time(distance, gender, age):
    '''
    returns graded time in decimal minutes for distance + gender + age
    '''
    time_t = str_to_time(records[distance][gender])
    graded_t = time_t/grades[distance][gender][age]
    return graded_t  

def graded_result(distance, gender, age):
    ''' 
    gets distance+gender+age and returns formatted time string 
    '''
    return time_to_str(get_dist_time(distance, gender, age))

def graded_percent(distance, gender, age, time_str):
    ''' 
    returns percentage of the Best Result for given age from distance+time+age 
    '''
    # 1) get overall record time
    record_t = str_to_time(records[distance][gender])
    # 2) convert overall record time to age-graded record time
    graded_record_t = record_t/grades[distance][gender][age]
    # 3) get diff between result and graded record
    graded_diff = graded_record_t/str_to_time(time_str)
    return str(round(graded_diff*100)) + '%'

def graded_distances(graded_percentage, age, gender):
    ''' 
    returns a list of probable results for a set of distances from age graded percentage
    '''
    ret_text = ''
    for distance in records.keys():
         print('graded_distances():', distance)        
         for d in DISTANCES.keys():
             if distance in DISTANCES[d]:
                 pretty_distance = DISTANCES[d][0]
                 break
         record_t        = str_to_time(records[distance][gender])
         graded_record_t = record_t/grades[distance][gender][age]
         age_graded_t    = graded_record_t/(graded_percentage/100)
         age_graded_str  = time_to_str(age_graded_t)
         ret_text += '{}: {}\n'.format(pretty_distance, age_graded_str)
    return ret_text


def build_agegraded(dist, res, age, gender):
    return graded_percent(dist, gender, age, res)

def build_agedist(percent, age, gender):
    return graded_distances(percent, age, gender)

### __main__ ###

if __name__ == '__main__':
    load_grade_files()
    executor.start_polling(dp)
