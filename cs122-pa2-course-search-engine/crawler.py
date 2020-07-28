# CS122: Course Search Engine Part 1
#
# Thomas Wilson
#

import re
import util
import bs4
import queue
import json
import sys
import csv
import requests

INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet'])


def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generate a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping of
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs:

    \

        CSV file of the index
    '''

    starting_url = ("http://www.classes.cs.uchicago.edu/archive/2015/winter"
                    "/12200-1/new.collegecatalog.uchicago.edu/index.html")
    limiting_domain = "classes.cs.uchicago.edu"


    queue = Queue()
    course_dict = {}
    analyze_page(starting_url, queue, limiting_domain, course_dict)


    counter = 1
    while not queue.isEmpty() and counter <= num_pages_to_crawl:
        counter += 1
        page = queue.dequeue()
        analyze_page(page, queue, limiting_domain, course_dict)

    convert_to_csv(course_dict)




class Queue:
    def __init__(self):
        self.items = []
        self.all_items = set()

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)
        self.all_items.add(item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def analyze_page(url, queue, limiting_domain, course_dict):
    '''
    Queues all urls, then makes a dictionary index of the course codes to
    a list of words in the course description.

    Inputs:
        url: the url of the page to analyze
        queue: the queue that holds the urls
        limiting_domain: a domain with which to stay in when queuing
        course_dict: the index dictionary

    Outputs:
        None
    '''
    request = util.get_request(url)
    text = util.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    queue_urls(url, soup, queue, limiting_domain)
    find_courses(soup, course_dict)

def queue_urls(url, soup, queue, limiting_domain):
    '''
    Forms a queue of all the urls

    Inputs:
        url: the url to put into the queue
        soup: BeautifulSoup object
        queue: the existing queue
        limiting_domain: a domain with which to stay in when queuing

    Outputs:
        None
    '''
    for link in soup.find_all('a'):
        clean_url = util.convert_if_relative_url(url, util.remove_fragment(link.get('href')))

        if util.is_absolute_url(clean_url) and str(clean_url)[0] != 'b':
            if (util.is_url_ok_to_follow(clean_url, limiting_domain)) and clean_url not in queue.all_items:
                queue.enqueue(clean_url)


def find_courses(soup, course_dict):
    '''
    Finds all of the course codes in a BeautifulSoup object and runs
    find_course_desc if the course code matches one in the json file.

    Inputs:
        soup(BeautifulSoup Object): the webpage html
        course_dict: the index dictionary

    Outputs:
        find_course_desc
    '''
    with open('course_map.json') as f:
        data = json.load(f)

    for tag in soup.find_all('div', 'courseblock main'):
        for title in tag.find_all('p', 'courseblocktitle'):
            match = re.search('[A-Z]{4} [0-9]{5}', title.text.encode('ascii', 'replace').decode('ascii').replace('?', ' '))
            if match:
                if match.group() in data:
                    course_code = data[match.group()]
                    return find_course_desc(tag, course_dict, course_code)

def find_course_desc(tag, course_dict, course_code):
    '''
    Adds words from the tag into the course dictionary

    Inputs:
        tag: Beautiful soup tag object: the tag that the course description is in
        course_dict: the dictionary that maps course codes words in the course description
        course_code: the code of the course

    Outputs:
        course_dict: course dictionary - updated with words from the tag
    '''
    if course_code not in course_dict:
        course_dict[course_code] = []
    for desc in tag.find_all('p', 'courseblockdesc'):
        for word in desc.text.split():
            word = word.lower()
            clean_word = remove_punctuation(word)
            if (clean_word not in INDEX_IGNORE) and (clean_word not in course_dict[course_code]):
                course_dict[course_code].append(clean_word)
    return course_dict

def remove_punctuation(string):
    '''
    removes punctuation if it's in the list of punctuation to remove

    inputs:
        string: a string

    outputs:
        no_punc: a string: a string with the punctuation removed
    '''
    punctuations = '''!()[]{};:"\,<>./?@#$%^&*_~'''
    no_punc = ''
    for char in string:
        if char not in punctuations:
            no_punc = no_punc + char
    return no_punc

def convert_to_csv(course_dict):
    '''
    turns course_dict into a csv file in the specified format

    inputs:
        course_dict: a dictionary

    outputs:
        None
    '''
    w = csv.writer(open("test.csv", "w"), delimiter = '|')
    for key, val in course_dict.items():
        for word in val:
            w.writerow([key, word])










if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    go(num_pages_to_crawl, course_map_filename, index_filename)
