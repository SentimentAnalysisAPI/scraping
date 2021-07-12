if __name__ == '__main__':
    ### adding FinancialSentiment directory to path
    import sys
    import os
    path = os.path.abspath(__file__)
    name = "FinancialSentiment"
    index = path.rfind(name) + len(name)
    path = path[:index]
    sys.path.append(path)

from utility.display import PrintJson
from utility.file import WriteJson

### https://praw.readthedocs.io/en/latest/index.html
import praw

def Main():
    prawReddit = PrawReddit()
    prawSubreddit = prawReddit.subreddit("wallstreetbets")
    # PrintJson(SubredditData(prawSubreddit))

    prawPosts = list(prawSubreddit.hot(limit=100))
    for prawPost in prawPosts[:3]:
        pass
        # PrintJson(PostData(prawPost))
    # prawPost = next(prawPosts)
    # PrintJson(PostData(prawPost))

def PrawReddit():
    ### https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html
    prawReddit = praw.Reddit(client_id="qfGgNSP41jjYdw",
        client_secret="1ebvBU9iD1-JnjHsVLYzKth6ntRd3w",
        user_agent="mybot")
    return prawReddit

def SubredditData(prawSubreddit):
    ### https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html
    return {
        "id": prawSubreddit.id,
        "name": prawSubreddit.display_name,
        "subscribers": prawSubreddit.subscribers
    }

def Posts(prawSubreddit, sort, limit):
    if sort == "hot": prawPosts = prawSubreddit.hot(limit=100)
    if sort == "new": prawPosts = prawSubreddit.new(limit=100)
    return prawPosts

def PostData(prawPost):
    ### https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    return {
        "id": prawPost.id,
        "name": prawPost.name,
        "title": prawPost.title,
        "url": prawPost.url,
        "timestamp": prawPost.url,
        "likes": prawPost.score,
        "dislikes": (prawPost.score / prawPost.upvote_ratio) - prawPost.score,
        "commentNum": prawPost.num_comments,
    }

if __name__ == '__main__':
    Main()