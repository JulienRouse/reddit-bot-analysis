""" Defines constants and namedtuple definitions"""
from collections import namedtuple

#from nltk.corpus import stopwords

#Enum for category
TOP = 0
HOT = 1

#namedtuple are awesome!
Score = namedtuple("Score", "total, ups, downs")
Post = namedtuple("Post", "id, title, author, comments, score")
Comment = namedtuple("Comment", "id, content, clean_content, author, score")

# loading french's stopwords an adding some more to fit into /r/france
FR = ["les", "si", "à", "a", "ils", "elles", "nous",
      "vous", "’", "ça", "là", "ca", "cela", "cette",
      "très", "comme", "quand", "être", "etre", "va",
      "avoir", "vraiment", "sans", "dire", "faire",
      "quoi", "tous", "leurs", "leur", "parce", "donc",
      "vu", "où", "ou", "puis", "chaque", "tant", "déjà",
      "dont", "mettre", "fais", "doit", "quel", "enfin",
      "vers", "ceux", "veux", "quelle", "pendant", "ni",
      "sait", "ah", "peu", "peux", "peut"]
""" :obj:`list` of :obj:`str`: French stopwords"""

EN = ["of", "in", "to", "i", "is", "you", "a", "the",
      "it", "we", "are", "an", "our", "this", "but",
      "will", "or", "if", "with", "your", "can", "for",
      "and", "that", "for", "my", "have", "at", "not",
      "they", "he", "she", "so", "has", "by", "us", "get",
      "was", "say", "other", "some", "what", "when", "where",
      "whom", "whose", "see", "much", "do", "would"]
""" :obj:`list` of :obj:`str`: English stopwords"""

URL = ["http", "https", "'", "...", "://", "com",
       "fr", "be", "www", ")[", "](", ").", "),", "org",
       ".)[", ",)[", ".](", ",]("]
""" :obj:`list` of :obj:`str`: Stopwords from url of weblinks"""

REDDIT = ["r", "u", "v", '",', "~", "~~", '".', "**", "¤"]
""" :obj:`list` of :obj:`str`: Stopwords that can be found on reddit"""

REMOVE_LIST = FR + EN + URL + REDDIT
""" :obj:`list` of :obj:`str`: The combination of every other stopwords lists"""

MY_STOPWORDS = set("")#stopwords.words('french'))
""" :obj:`set` of :obj:`str`: Stopwords in a set."""
MY_STOPWORDS.update(REMOVE_LIST)
