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
from utility.web import Soup

### https://praw.readthedocs.io/en/latest/index.html
import praw

params = [
    {
        "subreddit": "wallstreetbets",
        "sorts": ["hot", "new"],
        "maxPostNum": 2,
        "maxCommentNums": [3, 2]
    },
    {
        "subreddit": "finance",
        "sorts": ["hot", "new"],
        "maxPostNum": 3,
        "maxCommentNums": [5]
    },
    {
        "subreddit": "stocks",
        "sorts": ["hot", "new"],
        "maxPostNum": 3,
        "maxCommentNums": [5]
    }
]

def Reddit():
    prawReddit = PrawReddit()
    posts = []
    for param in params:
        prawSubreddit = prawReddit.subreddit(param["subreddit"])
        limit = param["maxPostNum"]
        for sort in param["sorts"]:
            if sort == "hot":
                prawPosts = prawSubreddit.hot(limit=limit)
            if sort == "new":
                prawPosts = prawSubreddit.new(limit=limit)
            if sort == "top":
                prawPosts = prawSubreddit.top(limit=limit)
            prawPosts = list(prawPosts)
            for prawPost in prawPosts:
                posts.append(PostData(prawPost, param["maxCommentNums"]))
    # PrintJson(SubredditData(prawSubreddit))
    return posts

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

def PostData(prawPost, maxCommentNums):
    print("New post")
    ### https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    data = {
        "id": prawPost.id,
        # "name": prawPost.name,
        "title": prawPost.title,
        "text": "\n".join(prawPost.selftext.split("\n")),
        "url": prawPost.url,
        "likes": prawPost.score,
        "dislikes": int((prawPost.score / prawPost.upvote_ratio) - prawPost.score),
        "commentNum": prawPost.num_comments,
        "time": int(prawPost.created_utc),
        "comments": []
    }
    prawComments1 = prawPost.comments[:maxCommentNums[0]]
    for prawComment1 in prawComments1:
        data["comments"].append({"text": FormatComment(prawComment1)})
        data["comments"][-1]["comments"] = []
        if len(maxCommentNums) == 1: continue
        prawComments2 = prawComment1.replies[:maxCommentNums[1]]
        for prawComment2 in prawComments2:
            data["comments"][-1]["comments"].append({"text": FormatComment(prawComment2)})
            data["comments"][-1]["comments"][-1]["comments"] = []
            if len(maxCommentNums) == 2: continue
            prawComments3 = prawComment2.replies[:maxCommentNums[2]]
            for prawComment3 in prawComments3:
                data["comments"][-1][-1].append({"text": FormatComment(prawComment3)})
    return data

def FormatComment(prawComment):
    try:
        text = Soup(prawComment.body_html).text.strip("\n")
    except: text = ""
    while "\n\n" in text: text = text.replace("\n\n", "\n")
    return text

if __name__ == '__main__':
    posts = Reddit(params[:1])
    PrintJson(posts)
