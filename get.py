from config import DISTANCES

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
