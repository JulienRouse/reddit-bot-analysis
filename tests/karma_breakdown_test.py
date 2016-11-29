from karma_breakdown import *
from nose import *

def setup_func():
    "set up test fixtures"
    pass

def teardown_func():
    "tear down test fixtures"
    pass

###############today_str########################################################
def today_str_test():
    """Test for today_str.
    The test is a bit pointless."""
    import datetime
    assert(today_str() == datetime.date.today().isoformat())

###############CLEAN_COMMENT####################################################
#@with_setup(setup_func, teardown_func)
#below is decorator to use setup and teardown
def clean_comment_test_empty():
    """Testing clean_comment with an empty string"""
    texts = ""
    expected = []
    assert(clean_comment(texts) == expected)

def clean_comment_test_valid_url():
    """Testing URL that should match. (valids URL)"""
    texts = ["http://www.randomurltotest.com",
             "http://www.randomurltotest.fr",
             "https://www.randomurltotest.com",
             "https://www.randomurltotest.fr",
             "www.randomurltotest.com",
             "www.randomurltotest.fr",
             "randomurltotest.com",
             "randomurltotest.fr",
             "aaa.randomurltotest.com",
             "aaa.randomurltotest.fr",
             "https://www.google.fr/search?q=google&ie=utf-8&oe=utf-8&client=firefox-b&gfe_rd=cr&ei=8Ek8WLLQNJDu8wfsjLuYBw"]
    expected = []
    for text in texts:
        yield valid_url_p, clean_comment(text), expected

def clean_comment_test_invalid_url():
    """Testing URL that should NOT match. (invalids URL)"""
    texts = [ "http://aaa.randomurltotest.com",
              "https://aaa.randomurltotest.com",
              "http://aaa.randomurltotest.fr",
              "https://aaa.randomurltotest.fr",
              "http://randomurltotest.com",
              "http://randomurltotest.fr",
              "mlksmlkdmqlskdmlsqmqlk"]
    not_expected = []
    for text in texts:
        yield invalid_url_p, clean_comment(text), not_expected

def valid_url_p(result, expected):
    """valid url predicate"""
    assert(result == expected)

def invalid_url_p(result, not_expected):
    """invalid url predicate"""
    assert(result != not_expected) 

def clean_comment_test_size_accepted():
    """Testing the size of the token that get accepted
    Only size >= 4 should pass"""
    text = "a aa aaa aaaa aaaaa aaaaaa" 
    expected = ["aaaaaa", "aaaaa", "aaaa"]
    assert(expected == clean_comment(text))

def clean_comment_test_stopwords_default():
    """Testing when you let stopwords at the default value (None).
    We give words that are in the stopwords and variation of them that are not.
    If everything is alright, only the variation should be in the return values.
    """
    text = "elles ellles temps tempss whose whosee"
    expected = ["whosee", "tempss", "ellles"]
    assert(expected == clean_comment(text))

def clean_comment_test_stopwords_as_parameters():
    """Testing when you pass stop-words as parameters.
    We give words that are in the stopwords and variation of them that are not.
    If everything is alright, only the variation should be in the return values.
    """
    param = ["ellles", "tempss", "whosee"]
    text = "elles ellles temps tempss whose whosee"
    expected = ["whose", "temps", "elles"]
    assert(expected == clean_comment(text, param))

############### ################################################################
