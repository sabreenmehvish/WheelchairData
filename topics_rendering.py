import jinja2
import os
import boto3
import botocore
import tarfile
import csv

def substitute_template(values):
    JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                              extensions=['jinja2.ext.autoescape'], autoescape=True)

    template = JINJA_ENVIRONMENT.get_template('topics_template.html')
    page = template.render(values = values)
    f = open("topics_page.html", "w")
    f.write(page)
    print(page)

def csv_to_dict(csv_path):
    topics_list = [{} for i in range(30)]
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                topic = int(row[0])
                term = row[1]
                confidence = float(row[2])
                topics_list[topic][term] = confidence
            line_count += 1
    return topics_list

def visualize_topics(job_name, output_path):
    values = {"job_name": job_name, "topics_list": csv_to_dict(output_path)}
    substitute_template(values)

