import boto3
s3 = boto3.resource('s3')
s3.Bucket('redditdocuments').upload_file('stopwords.txt', Key = "input")
