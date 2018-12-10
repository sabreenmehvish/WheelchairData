import praw
import json
import boto3
import os

s3 = boto3.resource('s3')


#enter reddit credentials here
reddit = praw.Reddit(client_id='ot3GaEquEnOMGg', \
                     client_secret='bIjzZxOdVUlmH-Ljdr4AqvLuv18', \
                     user_agent='scrapey', \
                     username='hcde_research', \
                     password='hcde_research')



def stripWordPunctuation(word):
    return word.strip(".,()<>\"\\'~?!;*:[]-+/`\u2014\u2018\u2019\u201c\u201d\u200b")

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


#----------bag of words----------#
#take a title, body, or comment "phrase"
#and a dictionary "word_dict"
#split into list of words
#strip words of punctuation and make lowercase
#put into word_dict
def bag_of_words(posts, job_name):
    word_dict = {}
    for post in posts:
        bag_of_words_phrase(post.title, word_dict)
        bag_of_words_phrase(post.selftext, word_dict)
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            bag_of_words_phrase(comment.body, word_dict)
        #writeFreqs(word_dict)
    return word_dict

#helper for bag_of_words
def bag_of_words_phrase(phrase, word_dict):
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

#----------one post per document-----------#
def post_per_document(posts, job_name):
    document_index = {}
    count = 0
    for post in posts:
        document = post.title + " " + post.selftext + " "
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            document += comment.body + " "
        sub = post.subreddit.display_name
        document_path = job_name + "/" + sub + str(count)
        document_index[document_path] = document
        count+=1
        print(document_path)
    return document_index

#take a dictionary of names and documents
#save value in .txt file, named with key
#optionally, upload the file to S3 bucket
def writeDocuments(document_index, should_upload):
    print("----Preparing documents for topic modelling----")
    for doc_name in document_index:
        doc_path = "documents/" + doc_name + ".txt"
        directory = os.path.dirname(doc_path)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)
        output = open(doc_path, "w", encoding='utf-8')
        output.write(document_index[doc_name])
        output.close()
        if should_upload:
            s3.Bucket('redditdocuments').upload_file(doc_path, Key=doc_path)
        print(doc_name)


#extracts reddit content from specified subreddits
#uses query provided with post_getter function
#names the folder job_name
#organizes text using specified method (e.g. bag of words, post per document)
def process_text(subreddit_list, post_getter, parsing_method, job_name):
    all_data = {}
    for subname in subreddit_list:
        print("----r/" + subname + "----")
        subreddit = reddit.subreddit(subname)
        sub_data = parsing_method(post_getter(subreddit), job_name)
        all_data.update(sub_data)
    writeDocuments(all_data, True)



#US city subreddits with >10k subscribers
us_cities = ["Seattle", "SeattleWA", "LosAngeles", "Boston", "NYC", "Portland", "Baltimore", "SanAntonio",
            "Phoenix", "SanJose", "Jacksonville", "Indianapolis", "Columbus", "Cincinnati",
            "Cleveland", "FortWorth", "Charlotte", "Detroit", "Vegas", "LasVegas", "Milwaukee", "Nashville",
            "Boulder", "Miami", "Oakland", "SaltLakeCity", "Huntsville", "Raleigh", "Chattanooga", "Minneapolis",
            "BayArea", "Sacramento", "Charleston", "Omaha", "Tucson", "ColoradoSprings", "Atlanta", "Chicago",
            "Dallas", "Houston", "Austin", "Denver", "Philadelphia", "Pittsburgh", "SanDiego", "SanFrancisco",
            "StLouis", "WashingtonDC", "rva", "NewOrleans", "KansasCity"]

disability = ["Disability", "Veterans"]

general = ["AskReddit", "legaladvice"]

def test():
    selected_subs = ["ADHD"]
    job_name = "ADHD_interface_2"
    process_text(selected_subs, lambda sub: sub.search("interface OR layout OR reading OR technology", limit = None), post_per_document, job_name)

#test()