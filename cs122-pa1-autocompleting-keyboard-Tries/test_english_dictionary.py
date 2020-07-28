# CS122: Auto-completing keyboard
# Test code for use with pytest
#
# Matthew Wachs
# Autumn 2014
#
# Revised: August 2015, AMR
#
# usage: py.test -xv [-k w/ keyword to limit the scope of the tests]

########################################
###                                  ###
###   DO NOT MODIFY THIS FILE        ###
###                                  ###
########################################

import pytest
import csv
import signal

try:
    module = __import__("english_dictionary")
except ImportError as ie:
    print("Could not import functions from english_dictionary.py")
    exit(1)

MAX_TIME = 200


def gen_scoring_code():
    all_funcs = []

    def points(weight):
        def wrap(f):
            all_funcs.append(f)
            f.weight = weight

            return f

        return wrap

    def handle_timeout(signum, frame):
        raise TimeoutError()

    def score_all_tests():
        points_accum = []

        for f in all_funcs:
            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(MAX_TIME)
            name = f.__name__
            weight = f.weight
            earned = 0
            try:
                f()
                earned = weight
            except TimeoutError as e:
                print("Timing out on ...", name)
            except Exception as e:
                print("hit exception", e)
            finally:
                signal.alarm(0)

            points_accum.append((name, earned, weight))

        return points_accum

    return points, score_all_tests


(weight, score_all_tests) = gen_scoring_code()

@weight(3.5)
def test_short_create_eng_dict():
    eng_dict = module.EnglishDictionary("five")
    assert(eng_dict is not None)

def helper_is_word(w, expected):
    eng_dict = module.EnglishDictionary("five")
    actual = eng_dict.is_word(w)
    assert(actual == expected)

@weight(1/4)
def test_short_is_word_0():
    helper_is_word("a", True)

@weight(1/4)
def test_short_is_word_1():
    helper_is_word("and", True)

@weight(1/4)
def test_short_is_word_2():
    helper_is_word("are", True)

@weight(1/4)
def test_short_is_word_3():
    helper_is_word("bee", True)

@weight(1/4)
def test_short_is_word_4():
    helper_is_word("ar", False)

@weight(1/4)
def test_short_is_word_5():
    helper_is_word("", False)

@weight(1/4)
def test_short_is_word_6():
    helper_is_word("foo", False)

@weight(1/4)
def test_short_is_word_7():
    helper_is_word("as", False)

def helper_num_completions(w, expected, eng_dict=None):
    if eng_dict is None:
        eng_dict = module.EnglishDictionary("five")
    actual = eng_dict.num_completions(w)
    assert(actual == expected)

@weight(1/4)
def test_short_num_completions_0():
    helper_num_completions("", 5)

@weight(1/4)
def test_short_num_completions_1():
    helper_num_completions("a", 4)

@weight(1/4)
def test_short_num_completions_2():
    helper_num_completions("an", 2)

@weight(1/4)
def test_short_num_completions_3():
    helper_num_completions("ar", 1)

@weight(1/4)
@pytest.mark.timeout(1)
def test_short_num_completions_4():
    helper_num_completions("and", 1)

@weight(1/4)
def test_short_num_completions_6():
    helper_num_completions("b", 1)

@weight(1/4)
def test_short_num_completions_7():
    helper_num_completions("as", 0)

def helper_get_completions(w, expected, eng_dict=None):
    if eng_dict is None:
        eng_dict = module.EnglishDictionary("five")
    actual = eng_dict.get_completions(w)
    actual = sorted(actual)
    expected = sorted(expected)
    assert(actual == expected)

@weight(1.75)
def test_short_get_completions_0():
    helper_get_completions("a", ["", "n", "nd", "re"])

@weight(1.75)
def test_short_get_completions_2():
    helper_get_completions("an", ["", "d"])

@weight(1.75)
def test_short_get_completions_3():
    helper_get_completions("and", [""])

@weight(1.75)
def test_short_get_completions_4():
    helper_get_completions("b", ["ee"])

@weight(1.75)
def test_short_get_completions_6():
        helper_get_completions("as", [])

import time

large_eng_dict = None

def build_large_eng_dict():
    global large_eng_dict
    if large_eng_dict is None:
        large_eng_dict = module.EnglishDictionary("web2")
    return large_eng_dict

@weight(3.5)
def test_long_create_eng_dict():
    build_large_eng_dict()

@weight(1.75)
def test_long_get_completions_0():
    eng_dict = build_large_eng_dict()
    helper_get_completions("aardv", ["ark"], eng_dict=eng_dict)

@weight(1.75)
def test_long_get_completions_1():
    eng_dict = build_large_eng_dict()
    helper_get_completions("nations", [], eng_dict=eng_dict)


@weight(1.75)
def test_long_get_completions_2():
    eng_dict = build_large_eng_dict()
    helper_get_completions("anticip",
                           ["atable", "ate", "ation", "ative", "atively",
                            "atorily", "ator", "atory", "ant"],
                           eng_dict=eng_dict)

@weight(1/4)
def test_long_num_completions():
    eng_dict = build_large_eng_dict()
    helper_num_completions("ar", 1417, eng_dict=eng_dict)

def print_result(scores):
    total_earned = 0
    total_available = 0

    for (name, earned, available) in sorted(scores):
        print("{}: {:.2f}/{:.2f}".format(name, earned, available))
        total_earned = total_earned + earned
        total_available = total_available + available

    print("\nTotal: {:.2f}/{:.2f}".format(total_earned, total_available))

def go():
    scores = score_all_tests()
    print_result(scores)

if __name__ == "__main__":
    go()
