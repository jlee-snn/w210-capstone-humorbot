import praw
import pandas as pd
import re
import contractions


reddit = praw.Reddit(client_id='cPX28na5fYf6Ng',
                     client_secret='Gz-TqIc0odjhelrx8E1WeXO8puE',
                     user_agent='myexploratoryapp1')


print(reddit.read_only)  # Output: True


subreddit = reddit.subreddit('jokes')
json_df = pd.read_json("reddit_jokes.json")
print(json_df.shape)

list_of_subreddits = ["cleanjokes","dadjokes","shortjokes","jokes","sciencejokes","ShortCleanFunny"]
titles = list()
body = list()
scores = list()
ids = list()

jokes_df = pd.DataFrame()

def Punctuation(string):

    # punctuation marks
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    # traverse the given string and if any punctuation
    # marks occur replace it with null
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")

    # Print string without punctuation
    print(string)

for ii in list_of_subreddits:
    subreddit = reddit.subreddit(ii)
    for submission in subreddit.top(limit=1000):
        # print(submission.title)  # Output: the submission's title
        # print(submission.score)  # Output: the submission's score
        # print(submission.id)     # Output: the submission's ID
        # print(submission.created)
        ids.append(submission.id)
        body.append(submission.selftext)
        scores.append(submission.score)
        titles.append(submission.title)

    for submission in subreddit.new(limit=1000):
        # print(submission.title)  # Output: the submission's title
        # print(submission.score)  # Output: the submission's score
        # print(submission.id)     # Output: the submission's ID
        # print(submission.created)
        ids.append(submission.id)
        body.append(submission.selftext)
        scores.append(submission.score)
        titles.append(submission.title)

    for submission in subreddit.hot(limit=1000):
        # print(submission.title)  # Output: the submission's title
        # print(submission.score)  # Output: the submission's score
        # print(submission.id)     # Output: the submission's ID
        # print(submission.created)
        ids.append(submission.id)
        body.append(submission.selftext)
        scores.append(submission.score)
        titles.append(submission.title)

jokes_df["id"] = ids
jokes_df["body"] = body
jokes_df["score"] = scores
jokes_df["title"] = titles
jokes_df = jokes_df.drop_duplicates()

#print(jokes_df.head())
#print(json_df.head())

total_df = pd.concat([jokes_df,json_df],axis = 0).drop_duplicates()
total_df = total_df
print(total_df)


clean_list = list()
for i in total_df["body"].values:
    #tmp = Punctuation(i)
    tmp = i.lower()
    tmp = contractions.fix(tmp)
    tmp = re.sub(r'[^A-Za-z0-9., ]+','', tmp)
    clean_list.append(tmp)

clean_titles = list()
for j in total_df["title"].values:
    #tmp = Punctuation(i)
    tmp = j.lower()
    tmp = contractions.fix(tmp)
    tmp = re.sub(r'[^A-Za-z0-9., ]+','', tmp)
    clean_titles.append(tmp)

total_df["body"] = clean_list
total_df["title"] = clean_titles
print(total_df)

total_df.to_csv("jokes_clean.csv")

# clean body
