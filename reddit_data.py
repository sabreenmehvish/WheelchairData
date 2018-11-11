import praw
import pandas as pd
import datetime as dt
import urllib.parse, urllib.request, urllib.error, json

def stripWordPunctuation(word):
    return word.strip(".,()<>\"\\'~?!;*:[]-+/`\u2014\u2018\u2019\u201c\u201d\u200b")

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

reddit = praw.Reddit(client_id='KA8wIsf92ExBVw', \
                     client_secret='js1n2d72q4lZeCwupToqezs4h-c', \
                     user_agent='scrapey', \
                     username='username', \
                     password='password')

#load <postnum> posts from specified subreddit
def extract_subreddit_text(subreddit, word_dict, postnum):
    print("----r/" + subreddit + "----")
    subreddit = reddit.subreddit(subreddit)
    for submission in subreddit.top(limit=postnum):
        parse_and_log(submission.title, word_dict)
        parse_and_log(submission.selftext, word_dict)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            parse_and_log(comment.body, word_dict)

#take a title, body, or comment "phrase"
#and a dictionary "word_dict"
#split into list of words
#strip words of punctuation and make lowercase
#put into word_dict
def parse_and_log(phrase, word_dict):
    #print(phrase)
    for word in phrase.split():
        word = stripWordPunctuation(word).lower()
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1

#take a bag of words
#check for stopwords and remove from bag
#write into a CSV file "freqs.csv"
def writeFreqs(freqdict):
    stopfile = open("stopwords.txt", "r")
    stopstring = stopfile.read()
    stoplist = stopstring.split()
    output = open("freqs.csv", "w", encoding='utf-8')
    output.write("word,instances\n")
    for word in freqdict:
        if word not in stoplist and \
                        freqdict[word] > 5 and \
                        len(word) > 0:
            csvline = word + "," + str(freqdict[word]) + "\n"
            print(csvline)
            output.write(csvline)

#take reddit content from specified subreddits
#load the top <postnum> posts and all of its comments
#log words into a CSV file
def reddit_bag_of_words(postnum, subreddit_list):
    word_dict = {}
    for subreddit in subreddit_list:
        extract_subreddit_text(subreddit, word_dict, postnum)
    writeFreqs(word_dict)

subreddits = ["Disability", "Wheelchairs"]
reddit_bag_of_words(100, subreddits)