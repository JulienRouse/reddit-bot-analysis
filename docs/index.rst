.. reddit-bot-analysis documentation master file, created by
   sphinx-quickstart on Sun Nov 27 11:46:41 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to reddit-bot-analysis's documentation!
===============================================

You're on the main page of the documentation here.
It is a work in progress, come back in a few days if you don't find the information you're seeking right now.

Also the project is only at about 50% completion so the documentation is subject to many changes.

What is it?
===========
There are two parts here.

First a Reddit bot that go on a subreddit and find either the newest posts or the top posts, download them and keep information about them.

Second a bunch of functions to gather metrics about the posts downloaded.
The goal is to dissect those post to be able to present meaningful data about them. I'd like to do some sentiment analysis, there is already a way to generate wordcloud out of the comments, and I'll see what can be done to expand on that.


Why?
====

I was curious and wanted to learn. 

Skills that I learned or practiced doing so (and the associated library if relevant):

- Building a reddit bot (praw)
- Building doc putting it on ReadTheDoc.org (sphinx, reStructuredText)
- Testing (nose)
- Regular expressions (re). Writing the regex for the URL was harder than expected, and it is still far from perfect. But it was a good remainder that they are handy tools that I should practice more often.
- Writing in english. I did publish a few blog posts about this project, writing a little bit more than 3000 words in the process. That's a lot for me and it's helping me improve.

Skills that I hope to learn/practice soon:

- Sentiment analysis (nltk probably)
- ?? 


Contents:

.. toctree::
   :maxdepth: 2
   
   install
   api
   roadmap
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

