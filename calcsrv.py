#!/usr/bin/python

import math
from config import DISTANCES

'''
vdot json server gets either:
- distance+time or
- VDOT as input
and returns:
- a json with VDOT for a given distance+time
- a list of times for a bunch of distances for a given VDOT
'''

def get_pace(dist, res):
    ''' returns pace for a given dist/res without leading hours: Mi:SS/km '''
    return time_to_str(res/(dist/1000))[3:]

def get_vdot(raw_vdot):
    ''' checks if vdot value is valid '''
    try:
        vdot = round(float(raw_vdot), 2)
    except:
        vdot = None
    return vdot

def get_dst(raw_dst):
    ''' checks if distance from a message is valid '''
    for d in DISTANCES.keys():
        if raw_dst.lower() in DISTANCES[d]:
            return DISTANCES[d][1]
    return None

def get_res(raw_res):
    ''' checks if result time from a message is valid '''
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
    ''' Balke 15 min running test '''
    if (distance < 100):
        return 'distance out of range'
    if (distance > 6500):
        return 'distance out of range'
    vo2max = 0.172 * (distance / 15 - 133) + 33.3
    return '{:2.2f}'.format(vo2max)

def cooper(distance):
    ''' cooper test from distance '''
    if (distance < 100):
        return 'distance out of range'
    if (distance > 5000):
        return 'distance out of range'
    vo2max = (distance - 504.9)/44.73
    return '{:2.2f}'.format(vo2max)

def cooper_from_time(str_time):
    ''' cooper test from time '''
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
    ''' the main function, converts distance+time to VDOT '''
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

def time_to_str(time):
    '''
    >>> time_to_str(123.45)
    02:03:27
    '''
    hours = time // 60
    secs, mins  = math.modf(time - hours*60)
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
