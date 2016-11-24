"""A reddit bot that survey /r/france for various analysis"""

# IMPORTANT
# When using in a REPL,
# either:
#    from filename import *
# or
#    from filename import Score, Post, Comment, ...
#
# If you dont, shelve/pickle will freak out cause it wont know the definition of those namedtuple.

#stdlib
from pprint import pprint
from collections import Counter
import shelve
import string

#3rd party lib
from nltk.tokenize import WordPunctTokenizer
import praw

#others project dependency
from model import Post, Comment, Score, MY_STOPWORDS, HOT, TOP


def load_counter(filename="save_counter"):
    """ Unshelve a counter from filename and returns it.
    Returns an empty counter if filename doesnt exist.

    Args:
        filename (str, optional): The name of the file to retrieve data from.
            Default is "save_counter".

    Returns:
        :obj:`Counter`: The counter object retrieved from filename or an empty counter.
    """
    res = Counter([])
    with shelve.open(filename) as database:
        res.update(database)
    return res

def save_counter(data, filename="save_counter"):
    """ Shelve data into filename.

    Args:
        data (:obj:`Counter`): A counter object to shelve.
            filename (str, optional): The name of the file where to shelve data to.
            Default is "save_counter".

    Returns:
        None
    """
    with shelve.open(filename) as database:
        database.update(data)

def load_data(filename="save_posts"):
    """ Unshelve a dict from filename.
    The dict contains data about Post objects retrieved from reddit.

    Args:
        filename (str, optional): The name of the file to retrieve the data from.
            Default is "save_posts".
    Returns:
        :obj:`dict`:
    """
    res = {}
    with shelve.open(filename) as database:
        res.update(database)
    return res

def save_data(data, filename="save_posts"):
    """Shelve data to filename

    Args:
        data (:obj:`dict`): The dict to be shelved.
            Keys are id(str) of posts objects, values are
            posts objects
        filename (str, optional): The name of the file where to sheve data to.
            Default is "save_posts".

    Returns:
        None
    """
    with shelve.open(filename) as database:
        database.update(data)

def clean_comment(comment, stopwords=None):
    """ Tokenize the string comment and remove various words in the stopwords list.
    Notably remove punctuation, numbers in the string, url,
    and various little french and english words.

    To get thoses words, see french_stopwords in Model.py

    The goal is to get a list of words that can be used for sentiment analysis.

    Args:
        comment (str): A string to be cleaned.
        stopwords (:obj:`list` of :obj:`str`, optional): A list of string to
        remove from the comment.

    Returns:
        :obj:`list`: List of clean words.
    """
    if stopwords is None:
        stopwords = MY_STOPWORDS
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(comment)
    res = []

    for token in tokens:
        token_low = token.lower()
        if (token_low not in stopwords and
                token_low not in string.punctuation and
                not token_low.isdigit()):
            res.insert(0, token_low)
    return res

def words_count_update(comment):
    """ Takes a clean comment and count words.
    It adds up to previous count.
    Also updates the shelve/pickle with the new count.

    Args:
        comment (list): A clean list of words.
            See the function clean_comment.

    Returns:
        Counter: A counter object, retrived with the function load_counter and
            updated with comment.

    See the functions clean_comment, load_counter and save_couter.
    """
    counter_words = load_counter()
    counter_words.update(comment)
    save_counter(counter_words)
    return counter_words


def search_reddit(subreddit="france", limit=100, category=HOT):
    """ Connect to reddit and gather posts from a subreddit.

    Note:
        Can be quite long (few minutes to run with limit=100) so cache it with save_data.

    Args:
        subreddit (str, optional): A string that designate an existing subreddit.
            Default is "france".
        limit (int, optional): Number of reddit posts to retrieve.
            Default is 100.
        category (int, optional): Either HOT or TOP. Those constants are defined in model.py.
            They determine if you gather post from the TOP (best posts ever)
            or HOT (newest posts) category.
            Default is HOT

    Returns:
        :obj:`Dict`: Return a dict of posts gathered. With key being the id of the post and value
            being the posts themselves.
    """
    user_agent = "Natural Language Processing:v0.1.0 (by /u/lughaidhdev)"
    reddit = praw.Reddit(user_agent=user_agent)
    subreddit_obj = reddit.get_subreddit(subreddit)
    posts = None
    if category == HOT:
        posts = subreddit_obj.get_hot(limit=limit)
    elif category == TOP:
        posts = subreddit_obj.get_top(limit=limit)
    else:
        print("ERROR: category must be either HOT or TOP, not ", category)
        return {}
    word_count = Counter()
    my_posts = {}
    for post in posts:
        thread = post.comments
        tmp_post = Post(id=post.id,
                        title=post.title,
                        author=post.author.name,
                        comments=[],
                        score=Score(total=post.score,
                                    ups=post.ups,
                                    downs=post.downs))
        for comment in thread:
            if isinstance(comment, praw.objects.MoreComments):
                pass
            else:
                if comment.body == "[deleted]" or comment.body == "[removed]":
                    pass
                else:
                    word_count.update(clean_comment(comment.body))
                    #words_count(clean_comment(comment.body))
                    tmp_comment = Comment(id=comment.id,
                                          content=comment.body,
                                          clean_content=clean_comment(comment.body),
                                          author=comment.author.name,
                                          score=Score(total=comment.score,
                                                      ups=comment.ups,
                                                      downs=comment.downs))
                    tmp_post.comments.insert(0, tmp_comment)
        my_posts[post.id] = tmp_post
    words_count_update(word_count)
    return my_posts

if __name__ == "__main__":
    RES = search_reddit()
    save_data(RES)

    COUNT = load_counter()

    pprint(COUNT.most_common(200))
