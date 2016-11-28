from karma_breakdown import *
from nose import *

def setup_func():
    "set up test fixtures"
    pass

def teardown_func():
    "tear down test fixtures"
    pass

@with_setup(setup_func, teardown_func)
def today_str_test():
    ""
    import datetime
    assert(today_str() == datetime.date.today().isoformat())


@with_setup(setup_func, teardown_func)
def clean_comment_test_url():
    ""
    pass
