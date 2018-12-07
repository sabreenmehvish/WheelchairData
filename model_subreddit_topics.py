import json
from bson import json_util
import reddit_data as reddittext
import topic_modelling
import topics_rendering
import os
import boto3
import botocore
import tarfile
import csv

def get_subreddit_topics(subreddits, query, job_name, num_topics):
    print("----Getting Reddit Data----")
    reddittext.process_text(subreddits,
                            lambda sub: sub.search(query, limit = None),
                            reddittext.post_per_document, job_name)
    print("----Creating topic modelling job----")
    output_path = topic_modelling.run_topic_model(job_name, num_topics)
    if not os.path.isdir(output_path[:-13]):
        os.makedirs(output_path[:-13])
    topics_rendering.visualize_topics(job_name, get_topics_file(output_path))

def get_topics_file(filepath):
    BUCKET_NAME = 'redditdocuments'  # replace with your bucket name
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file(filepath, filepath)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    tar = tarfile.open(filepath)
    topics_dir = os.path.dirname(filepath)
    tar.extractall(path = topics_dir)
    tar.close()
    return topics_dir + "/topic-terms.csv"



