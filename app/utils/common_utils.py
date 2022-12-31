
import calendar
import datetime
import json
import csv

from consts.common_consts import *

def create_yesterday_date() -> str:
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    dd = datetime.datetime.now(JST)
    yy = dd - datetime.timedelta(days=1)
    return yy.strftime('%Y-%m-%d')

def create_today() -> str:
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    dd = datetime.datetime.now(JST)
    return dd.strftime('%Y-%m-%d %H:%M:%S')

def get_int( value ):
    return int(value) if value is not None else None

def get_float( value ):
    return float(value) if value is not None else None

def dict_to_json( dict ):
    return json.dumps( dict ) if dict is not None else None

def json_to_dict( json_str ):
    return json.loads( json_str )
    
def parse_csv( csv_str ):

    import csv
    lines = []
    for temp_line in csv.reader(csv_str.splitlines()):
        if 1 < len( temp_line ):
            lines.append( temp_line )
    return lines
'''
    lines = []
    for line in csv_str.split("\n"):
        temp_line = line.split(",")
        if 1 < len( temp_line ):
            lines.append( temp_line )

    return lines
'''