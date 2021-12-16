from datetime import datetime, date
from math import floor

def datetimeformat(value, format='%b. %d, %Y'):
    return value.strftime(format)

def strfdelta(tdelta, format='{years} years, {months} months, {days} days'):
    #print(tdelta)
    d = {'days':tdelta.days}
    total_days = d['days']
    y = floor(total_days/365)
    total_days %= 365
    m = floor(total_days / 30)
    output = ""
    if y > 0:
        output += str(y) + ' years, '
    if m > 0:
        output += str(m) + ' months ' 
    else:
        output += str(d['days']) + ' days '
    output += 'ago!'
    return output


def datetimepassed(value):
    now = datetime.now()
    time_difference = now - value
    return strfdelta(time_difference)


def get_class(obj):
    return obj.__class__.__name__