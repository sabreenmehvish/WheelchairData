import jinja2
import os
import csv

def substitute_template(values):
    JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                              extensions=['jinja2.ext.autoescape'], autoescape=True)

    template = JINJA_ENVIRONMENT.get_template('topics_template.html')
    page = template.render(values = values)
    return page

def csv_to_dict(topic_files_dir, num_topics):
    topics_list = [{'documents': {}, 'terms': {}} for i in range(num_topics)]
    topic_terms_path = os.path.join(topic_files_dir, "topic-terms.csv")
    doc_topics_path = os.path.join(topic_files_dir, "doc-topics.csv")
    with open(topic_terms_path) as topic_terms_file:
        csv_reader = csv.reader(topic_terms_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                topic = int(row[0])
                term = row[1]
                confidence = float(row[2])
                topics_list[topic]['terms'][term] = confidence
            line_count += 1

    with open(doc_topics_path) as doc_topics_file:
        csv_reader = csv.reader(doc_topics_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                document = row[0]
                topic = int(row[1])
                confidence = float(row[2])
                topics_list[topic]['documents'][document] = confidence
            line_count += 1
    return topics_list


