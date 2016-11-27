"""A reddit bot for various analysis"""
#stdlib
#from pprint import pprint
from collections import Counter
from datetime import date
import shelve
import string
import os

#3rd party lib
from nltk.tokenize import WordPunctTokenizer
from wordcloud import WordCloud
from PIL import Image
import praw
import matplotlib.pyplot as plt
import numpy as np

#others project dependency
from model import Post, Comment, Score, MY_STOPWORDS, HOT, TOP

###############CODE############################################################
def today_str():
    """ The date of today in isoformat. i.e. '2016-11-26'"""
    return date.today().isoformat()

def load_counter(filename="counter" + today_str(), dirname="save"):
    """ Unshelve a counter from filename and returns it.
    Returns an empty counter if filename doesnt exist.

    Args:
        filename (:obj:`str`, optional): The name of the file to retrieve data from.
            Default is "counter" + today_str().
            today_str returns the date of today with the isoformat. i.e. "2016-11-22"
        dirname (:obj:`str`, optional): The name of the dir to retrieve data from.
            Default is "save"
    Returns:
        :obj:`Counter`: The counter object retrieved from filename or an empty counter.
    """
    res = Counter([])
    with shelve.open(os.path.join(dirname, filename)) as database:
        res.update(database)
    return res

def save_counter(data, filename="counter" + today_str(), dirname="save"):
    """ Shelve data into filename.

    Args:
        data (:obj:`Counter`): A counter object to shelve.
        filename (:obj:`str`, optional): The name of the file where to shelve data to.
            Default is "counter".
            today_str returns the date of today with the isoformat. i.e. "2016-11-22"
        dirname (:obj:`str`, optional): The name of the dir where to shelve data to.
            Default is "save"

    Returns:
        None: Nothing.
    """
    with shelve.open(os.path.join(dirname, filename)) as database:
        database.update(data)

def load_data(filename="posts" + today_str(), dirname="save"):
    """ Unshelve a dict from filename.
    The dict contains data about Post objects retrieved from reddit.

    Args:
        filename (:obj:`str`, optional): The name of the file to retrieve the data from.
            Default is "posts" + today_str().
            today_str returns the date of today with the isoformat. i.e. "2016-11-22"
        dirname (:obj:`str`, optional): The name of the dir to retrieve the data from.
            Default is "save"
    Returns:
        :obj:`dict`: Dictionary containing data about Post. 
    """
    if not os.path.isfile(os.path.join(dirname, filename)):
        data = search_reddit()
        save_data(data, filename=filename, dirname=dirname)
    res = {}
    with shelve.open(os.path.join(dirname, filename)) as database:
        res.update(database)
    return res

def save_data(data, filename="posts" + today_str(), dirname="save"):
    """Shelve data to filename

    Args:
        data (:obj:`dict`): The dict to be shelved.
            Keys are id(:obj:`str`) of posts objects, values are
            posts objects
        filename (:obj:`str`, optional): The name of the file where to sheve data to.
            Default is "posts" + today_str().
            today_str returns the date of today with the isoformat. i.e. "2016-11-22"
        dirname (:obj:`str`, optional): The name of the dire where to whelve data to.
            Default is "save"

    Returns:
        None: Nothing
    """
    with shelve.open(os.path.join(dirname, filename)) as database:
        database.update(data)

def clean_comment(comment, stopwords=None):
    """ Tokenize the string comment and remove various words in the stopwords list.
    Notably remove punctuation, numbers in the string, url,
    and various little french and english words.

    To get thoses words, see french_stopwords in Model.py

    The goal is to get a list of words that can be used for sentiment analysis.

    Args:
        comment (:obj:`str`): A string to be cleaned.
        stopwords (:obj:`list` of :obj:`str`, optional): A list of string to
        remove from the comment.

    Returns:
        :obj:`list` of :obj:`str`: List of clean words.
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
        comment (:obj:`list`): A clean list of words.
            See the function clean_comment.
    Returns:
        :obj:`Counter`: A counter object, retrived with the function load_counter and
        updated with comment.
    See also:
        clean_comment
        load_counter
        save_counter
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
        subreddit (:obj:`str`, optional): A string that designate an existing subreddit.
            Default is "france".
        limit (:obj:`int`, optional): Number of reddit posts to retrieve.
            Default is 100.
        category (:obj:`int`, optional): Either HOT or TOP. Those constants are defined in model.py.
            They determine if you gather post from the TOP (best posts ever)
            or HOT (newest posts) category.
            Default is HOT.

    Returns:
        :obj:`dict`: Return a dict of posts gathered. With key being the id of the post and value
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

def extract_comment(data):
    """ Takes a dict of Post and returns the concatenation of all the comment
    of the Posts cleaned into a string

    Args:
        data (:obj:`dict`): The data to extract comment from.
             The key/value pair is of type :obj:`str`/:obj:Post.

    Returns:
        :obj:`str`: A text composed of all the clean comment gathered in data.
    """
    res = []
    for post in data.values():
        for comment in post.comments:
            res.insert(0, comment.clean_content)

    res = [item for sublist in res for item in sublist]
    text = " ".join(res)
    return text

def create_mask(filename):
    """ Create a mask from an image
    Idea comes from https://github.com/amueller/word_cloud/blob/master/examples/masked.py

    Args:
        filename (:obj:`str` or None): The name of the file to create a mask with.
            If None, returns None.

    Returns:
        :obj:`np.array` or None: An array defining the shape of the image.
        Or None is filename=None.
    """
    if filename is None:
        return None
    directory = "img"
    mask = np.array(Image.open(os.path.join(directory, filename)))
    return mask

def show_wordcloud(wordcloud):
    """ Create a plot with wordcloud and displays it.

    Args:
        wordcloud (:obj:`WordCloud`): A WordCloud object. See module wordcloud.

    Returns:
        None: Side effect is showing a plot on screen.
    """
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

def save_wordcloud(wordcloud, filename="wordcloud.jpg", dirname="wordcloud"):
    """ Create a plot with wordcloud and save it in dirname/filename
    Also creates dirname if not found.

    Args:
        wordcloud (:obj:`WordCloud`): A WordCloud object. See module wordcloud.
        filename (:obj:`str`, optional): The name to save the file to.
            Default is "wordcloud.jpg".
        dirname (:obj:`str`, optional): The name of the dir to save the file to.
            Default is "wordcloud".

    Returns:
        None: Side effect is creates a file, and if dirname did not exist, creates dirname.
     
    """
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(dirname + os.sep + filename)

def generate_wordcloud(text, background_color="white", mask=None, max_words=500, savefilename=None):
    """ Create and save a wordcloud.

    Args:
        text (:obj:`str`): A text to makes a wordcloud from.
        background_color (:obj:`str`, optional): The string represents known color to matplolib.
            Define the background color of the wordcloud.
            Default is "white".
        mask (:obj:`str` or None, optional): The name of the file to create the mask
            to apply to the wordcloud if you want it to not be a rectangle or None for no mask.
            Default is None.
        max_words (:obj:`int`, optional): Maximum of words to consider when creating
            the wordcloud from the text.
            Default is 500.

    Returns:
        None
    """
    mask = create_mask(mask)
    word_cloud = WordCloud(background_color=background_color,
                           max_words=max_words,
                           mask=mask).generate(text)
    save_wordcloud(word_cloud, filename=savefilename)

if __name__ == "__main__":
    RES = search_reddit()
    save_data(RES)


    DATA = load_data()
    TEXT = extract_comment(DATA)
    FILE = "alice.jpg"
    generate_wordcloud(TEXT, mask=FILE, savefilename=FILE)
    #COUNT = load_counter()
    #pprint(COUNT.most_common(200))
