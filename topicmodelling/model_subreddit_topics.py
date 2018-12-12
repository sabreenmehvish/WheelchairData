import json
import reddit_data as reddittext
import topic_modelling
import topics_rendering
import os
import boto3
import botocore
import tarfile

basedir = os.path.dirname(os.path.abspath(__file__))

def get_subreddit_topics_jinja(subreddits, query, job_name, num_topics):
    values = get_subreddit_topics(subreddits, query, job_name, num_topics)
    page = topics_rendering.substitute_template(values)

def get_subreddit_topics(subreddits, query, job_name, num_topics):
    print("----Getting Reddit Data----")
    reddittext.process_text(subreddits,
                            lambda sub: sub.search(query, limit=None),
                            reddittext.post_per_document, job_name)
    print("----Creating topic modelling job----")
    output_path = topic_modelling.run_topic_model(job_name, num_topics)
    if not os.path.isdir(os.path.join(basedir, output_path[:-13])):
        os.makedirs(os.path.join(basedir, output_path[:-13]))
    values = {"job_name": job_name,
              "topics_list": topics_rendering.csv_to_dict(get_topics_files(output_path), num_topics)}
    return values

def get_topics_files(filepath):
    BUCKET_NAME = 'redditdocuments'  # replace with your bucket name
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file(filepath, os.path.join(basedir, filepath))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    tar = tarfile.open(os.path.join(basedir, filepath))
    topics_dir = os.path.dirname(os.path.join(basedir, filepath))
    tar.extractall(path = topics_dir)
    tar.close()
    return topics_dir

