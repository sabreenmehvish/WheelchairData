import boto3
import botocore
import json
from bson import json_util
import reddit_data as reddittext
from polling import TimeoutException, poll

def getJobStatus(comprehend, job_description):
    return comprehend.describe_topics_detection_job(
        JobId=job_description['JobId'])


def checkJobDone(comprehend, job_description):
    return getJobStatus(comprehend,
                        job_description)['TopicsDetectionJobProperties']['JobStatus'] \
                        in ['COMPLETED', 'FAILED']


def run_topic_model(job_name, num_topics):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    input_s3_url = "s3://redditdocuments/documents/" + job_name
    input_doc_format = "ONE_DOC_PER_FILE"
    output_s3_url = "s3://redditdocuments/analysis/" + job_name
    data_access_role_arn = "insert_arn"
    number_of_topics = num_topics

    input_data_config = {"S3Uri": input_s3_url, "InputFormat": input_doc_format}
    output_data_config = {"S3Uri": output_s3_url}

    start_topics_detection_job_result = \
        comprehend.start_topics_detection_job(NumberOfTopics=number_of_topics,
                                                                              InputDataConfig=input_data_config,
                                                                              OutputDataConfig=output_data_config,
                                                                              DataAccessRoleArn=data_access_role_arn)
    print("----Topic modelling job started----")
    try:
        poll(lambda: checkJobDone(comprehend, start_topics_detection_job_result), timeout=3000, step=1)
    except TimeoutException as tee:
        print("Value was not registered")
    print("----Topic modelling job finished----")
    status = getJobStatus(comprehend, start_topics_detection_job_result)
    output_path = status['TopicsDetectionJobProperties']['OutputDataConfig']['S3Uri'][21:]
    return output_path
