import boto3
import json
from bson import json_util
import reddit_data as reddittext


subreddits = ["Disability"]
job_name = "disability_1"
reddittext.process_text(subreddits,
                        lambda sub: sub.search("wheelchair"),
                        reddittext.post_per_document, job_name)


print("----Running comprehend----")
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

input_s3_url = "s3://redditdocuments/documents/" + job_name
input_doc_format = "ONE_DOC_PER_FILE"
output_s3_url = "s3://redditdocuments/analysis/" + job_name
data_access_role_arn = "arn"
number_of_topics = 20

input_data_config = {"S3Uri": input_s3_url, "InputFormat": input_doc_format}
output_data_config = {"S3Uri": output_s3_url}

start_topics_detection_job_result = comprehend.start_topics_detection_job(NumberOfTopics=number_of_topics,
                                                                          InputDataConfig=input_data_config,
                                                                          OutputDataConfig=output_data_config,
                                                                          DataAccessRoleArn=data_access_role_arn)

print("----Request sent----")