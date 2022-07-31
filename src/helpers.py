# import praw
# from tqdm import tqdm
# from praw.models import MoreComments
# import pandas as pd
# import numpy as np
# import re
# import nltk.corpus
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# from config import REDDIT_ID, REDDIT_NAME, REDDIT_SECRET

# reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent=REDDIT_NAME) 
# wsb = reddit.subreddit('wallstreetbets')


# post_wrd_freq = {}
# posts = []

# def iterator(words):
#     '''
#     iterates through block of text and gets word frequency and
#     places into above dictionary
#     '''
#     # NLTK stopwords
#     stop = stopwords.words('english')
#     # Remove punctuation and links
#     words = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", words)
#     # make lowercase and remove stopwords
#     words = " ".join([word for word in words.split() if word not in (stop)]).lower() 
    
#     for word in words.split():
#         # print(word)
#         if word not in post_wrd_freq:
#             post_wrd_freq[word] = 1
#         else:
#             post_wrd_freq[word] += 1

# for post in wsb.hot(limit=100):
#     posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
# posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
# # print(posts)

# for column in tqdm(posts["id"]):
#     submission = reddit.submission(id=column)
#     # submission.comments.replace_more(limit=0)
#     iterator(posts.loc[posts['id'] == column, 'body'].values[0])
#     # for comment in submission.comments.list():
#     #     iterator(comment.body)
#     # for top_level_comment in submission.comments:
#     #     if isinstance(top_level_comment, MoreComments):
#     #         continue
#     #     iterator(top_level_comment.body)
#         # now try to make something to save these bodies and look at what stocks
#         # are being talked about the most and if buy, sell, and hold is being used with them
# print(post_wrd_freq)
# print(sorted(post_wrd_freq, key=post_wrd_freq.get, reverse=True)[:5])
# # make it so it has to go through a stock ticker checker/company checker before adding to dict

from datetime import datetime
import time


def checkTime():
    # This function runs periodically every 1 second
    time.sleep(1)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    return current_time

    # if(current_time == '09:30:00'):  # check if matches with the desired time
    #     print('sending message')
    #     while current_time != '16:00:00':
    #         print("hi") # make a conditional to run a specific method given user input
