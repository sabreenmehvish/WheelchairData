import jinja2
import os
import boto3
import botocore
import tarfile
import csv

def generate_page(topics):
    JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                              extensions=['jinja2.ext.autoescape'], autoescape=True)

    #topics = [{"read": .2, "listen": .3, "comprehend": .5}, {"social": .4, "anxiety": 3, "talk": .3}]
    template = JINJA_ENVIRONMENT.get_template('topics_template.html')
    page = template.render(topics_list = topics)
    f = open("topics_page.html", "w")
    f.write(page)
    print(page)

def get_topics_file():
    BUCKET_NAME = 'redditdocuments'  # replace with your bucket name
    KEY = ''  # replace with your object key
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file('analysis/ADHD_interfaces_2/449600645648-TOPICS-d230824d218ba8ef6f4be8c7664c2a0f/output/output.tar.gz', "topic_outputs/output.tar.gz")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def unzip_topics_file():
    tar = tarfile.open("topic_outputs/output.tar.gz", "r:gz")
    tar.extractall(path = "topic_outputs")
    tar.close()

def csv_to_dict():
    topics_list = [{} for i in range(30)]
    with open('topic_outputs/topic-terms.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                topic = int(row[0])
                term = row[1]
                confidence = float(row[2])
                topics_list[topic][term] = confidence
            line_count += 1
    #print(topics_list)
    return topics_list

generate_page(csv_to_dict())