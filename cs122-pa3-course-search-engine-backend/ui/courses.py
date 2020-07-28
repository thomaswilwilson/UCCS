### CS122, Winter 2019: Course search engine: search
###
### Thomas Wilson

from math import radians, cos, sin, asin, sqrt
import sqlite3
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')

def find_courses(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept a string
      - day a list with variable number of elements
           -> ["'MWF'", "'TR'", etc.]
      - time_start an integer in the range 0-2359
      - time_end an integer in the range 0-2359
      - walking_time an integer
      - enroll_lower an integer
      - enroll_upper an integer
      - building a string
      - terms a string: "quantum plato"]

    Returns a pair: list of attribute names in order and a list
    containing query results.
    '''
    sections = {
        'courses': {'catalog_index': 'course_id', 'sections': 'course_id'},
        'meeting_patterns': {'sections': 'meeting_pattern_id'},
        'gps': {'sections': 'building_code'},
        'catalog_index': {'courses': 'course_id'},
        'sections': {'meeting_patterns': 'meeting_pattern_id', 'courses': 'course_id', 'gps': 'building_code'},
    }

    d = {
        'terms': ['courses.dept', 'courses.course_num', 'courses.title'], 
        'dept': ['courses.dept', 'courses.course_num', 'courses.title'],
        'day': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end'],
        'time_start': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end'],
        'time_end': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end'],
        'walking_time': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end', 'a.building_code'],
        'building': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end', 'b.building_code'],
        'enroll_lower': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end','sections.enrollment'],
        'enroll_upper': ['courses.dept', 'courses.course_num', 'sections.section_num', 'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end','sections.enrollment']
    }

    schema = {
        'courses': ['course_id', 'dept', 'course_num', 'title'],
        'sections': ['section_id', 'course_id', 'section_num', 'meeting_pattern_id', 'building_code', 'enroll_lower', 'enroll_upper'],
        'meeting_patterns': ['meeting_pattern_id', 'day', 'time_start', 'time_end'],
        'gps': ['building_code', 'lat', 'lon'],
        'catalog_index': ['course_id', 'word', 'terms']
    }

    if args_from_ui == {}:
        return ([], [])

    db = sqlite3.connect(DATABASE_FILENAME)
    db.create_function("time_between", 4, compute_time_between)
    c = db.cursor()
    s = get_string(args_from_ui, schema, d, sections)

    args = get_args(args_from_ui)

    r = c.execute(s,args)

    return (clean_header(get_header(r)), r.fetchall())


    # replace with a list of the attribute names in order and a list
    # of query results.
    # return ([], [])


########### auxiliary functions #################
def get_select(input_dict, d):
    '''
    Takes the user's input dictionary and retuns a list of all attributes that
    must be selected.

    inputs:
        input_dict(dict): dictionary containing search criteria
        d(dict): dictionary that represents the relationships between the
        search criteria and the artibutes that must be selected

    returns:
        l(list): list of attributes
    '''
    l = []
    output_l = ['courses.dept', 'courses.course_num', 'sections.section_num', 
    'meeting_patterns.day', 'meeting_patterns.time_start', 'meeting_patterns.time_end','b.building_code', 
    'time_between(a.lon, a.lat, b.lon, b.lat) AS walking_time','sections.enrollment', 'courses.title']
    
    if 'walking_time' in input_dict.keys():
        l.append('time_between(a.lon, a.lat, b.lon, b.lat) AS walking_time')

    for key, value in input_dict.items():
        if key != 'walking_time':
            for attribute in d[key]:

                if attribute not in l:
                    l.append(attribute)

    l = sorted(l, key = lambda x: output_l.index(x))  

    return l


def get_join(select_list, sections):
    '''
    Takes the attributes that must be selected and returns the tables that
     must be join

    inputs:
        select_list(lst): a list containing the attributes that must be
         selected
        sections(dict): dictionary that represents the keys that each table
         must be joined on

    returns:
        l(list): list of the tables that hae to be joined
    '''
    l = []

    for i in select_list:

        for j in i.split('.'):

            if j not in l and j in sections and j != 'a':
                l.append(j)

    return l


def get_on(input_dict, join_list, sections):
    '''
    Takes the user's input dictionary, the list of tables that have to be
     joined and a dictionary of the keys that tables should joined on and
     returns a list of the ON's as well as calls bridge_gaps which ensures
      that we are joining all nessecary tabels

    inputs:
        input_dict(dict): dictionary containing search criteria
        sections(dict): dictionary that represents the keys that each
         table should be joined on
        join_list(lst): list of tables that have to be joined

    returns:
        l(list): list of attributes
    '''
    bridge_gaps(input_dict, join_list)
    l = []



    for c, value in enumerate(join_list):
        if value:
            if c != 0:
                pv = join_list[c-1]

                if pv in sections[value].keys():
                    on = value + '.' + sections[value][pv]
                    on += ' = ' + pv + '.' + sections[value][pv]

                elif value in sections['sections'].keys():
                    on = value + '.' + sections['sections'][value]
                    on +=' = sections.' + sections['sections'][value]

                elif value in sections['courses'].keys():
                    on = value + '.' + sections['courses'][value] 
                    on += ' = sections.' + sections['courses'][value]
                l.append(on)

    if 'walking_time' in input_dict.keys():
        l.append('sections.building_code = b.building_code')
        join_list.append('gps AS a')
        join_list.append('gps AS b')

    return l




def bridge_gaps(input_dict, join_list):
    '''
    Takes the user's input dictionary the list of tables that need to be
     joined and updates the list to ensure that every table that we need gets
     joined

    inputs:
        input_dict(dict): dictionary containing search criteria
        join_list(lst): list of tables that have to be joined

    returns:
        None
    '''
    if 'meeting_patterns' in join_list and 'sections' not in join_list:
        join_list.append('sections')

    if 'gps' in join_list and 'sections' not in join_list:
        join_list.append('gps')

    if 'catalog_index' in join_list and 'courses' not in join_list:
        join_list.append('courses')

    if 'terms' in input_dict.keys():
        join_list.append('catalog_index')




def get_where(input_dict, schema):
    '''
    Takes the user's input dictionary and a dictionary that represents all of
     the relationships in the schema and constructions a list of all of the
     WHERE statements
    
    inputs:
        input_dict(dict): dictionary containing search criteria
        schema(dict): dictionary that represents all of the relationships of 
        the schema

    returns:
        lst(lst): list of all of the nessecary WHERE statements
    '''
    lst = []

    for key in input_dict.keys():
        for table in schema:

            if key in schema[table]:
                if key == 'time_start':
                    lst.append(table + '.' + key + ' >= ' + ' ?')
                if key == 'time_end':
                    lst.append(table + '.' + key + ' <= ' + ' ?')
                if key == 'enroll_lower':
                    lst.append(table + '.' + 'enrollment' + ' >= ' + ' ?')
                if key == 'enroll_upper':
                    lst.append(table + '.' + 'enrollment' + ' <= ' + ' ?')
                if key == 'day':
                    lst.append(get_day(input_dict[key] ,table))
                if key == 'dept':
                    lst.append('courses.dept = ?')
                if key == 'terms':
                    if len(input_dict['terms'].split(" ")) == 1:
                        lst.append(table + '.word = ? ')
                    else:
                        prefix = ' courses.course_id IN (SELECT catalog_index.course_id FROM catalog_index WHERE word = '
                        suf = ' AND courses.course_id IN (SELECT catalog_index.course_id FROM catalog_index WHERE word = '
                        suf = suf.join(['?)' for x in input_dict['terms'].split(" ")])
                        lst.append(prefix + suf)

    if 'walking_time' in input_dict.keys():
        lst.append('a.building_code = ?')
        lst.append('walking_time <= ?')

    return lst



def get_string(input_dict, schema, d, sections):
    '''
    Takes the input dict and schema and constructs the entire string for the
    sqlite3 query

    inputs:
        input_dict(dict): dictionary containing search criteria
        schema(dict): dictionary that represents all of the relationships of 
        the schema

    returns:
        sqlite3 query string
    '''
    select =  get_select(input_dict, d)
    join = get_join(select, sections)
    on = get_on(input_dict, join, sections)
    where = get_where(input_dict, schema)
    if_on = ''
    if on:
        if_on = ' ON '

    return 'SELECT DISTINCT ' + ', '.join(select) + ' FROM ' + ' JOIN '.join\
    (join) + if_on + ' AND '.join(on) + ' WHERE ' + ' AND '.join(where)


def get_day(day_list, table):
    '''
    constructs the WHERE query if we are looking for day

    inputs:
        day_list(lst): list of all of the days we're seaching for
        table(string): name of the day table

    returns:
        string for the day query
    '''
    day_labels = [table + '.day = ?' for x in day_list]
    day = '(' + ' OR '.join(day_labels) + ')'
    return day

def get_term(terms):
    '''
    constructs the WHERE query if we are looking for terms

    inputs:
        day_list(lst): list of all of the terms

    returns:
        string for the terms query
    '''
    terms = ['catalog_index.word = ?' for x in terms]
    return ' AND '.join(terms)

def get_args(args_from_ui):
    '''
    given the input dictionary, returns the list of arguments for the query

    input:
     args_from_ui(dict): dictionary containing search criteria

    returns:
     args(lst): list of arguments
    '''
    l = []
    args = []
     
    for key, item in args_from_ui.items():

        if key == 'day':
            for day in item:

                l.append(day)

        if key not in ['building', 'walking_time']:
            l.append(item)

    for i, arg in enumerate(l):

        if type(arg) == str:
            for word in arg.split(" "):

                args.append(word)

        else:
            args.append(arg)

    if 'walking_time' in args_from_ui.keys():
        args.append(args_from_ui['building'])
        args.append(args_from_ui['walking_time'])

    return args

########### do not change this code #############

def compute_time_between(lon1, lat1, lon2, lat2):
    '''
    Converts the output of the haversine formula to walking time in minutes
    '''
    meters = haversine(lon1, lat1, lon2, lat2)

    # adjusted downwards to account for manhattan distance
    walk_speed_m_per_sec = 1.1
    mins = meters / (walk_speed_m_per_sec * 60)

    return mins


def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the circle distance between two points
    on the earth (specified in decimal degrees)
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    m = km * 1000
    return m


def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i, _ in enumerate(s):
        if s[i] == ".":
            s = s[i + 1:]
            break

    return s


########### some sample inputs #################

EXAMPLE_0 = {"time_start": 930,
             "time_end": 1500,
             "day": ["MWF"]}

EXAMPLE_1 = {"dept": "CMSC",
             "day": ["MWF", "TR"],
             "time_start": 1030,
             "time_end": 1500,
             "enroll_lower": 20,
             "terms": "computer science"}