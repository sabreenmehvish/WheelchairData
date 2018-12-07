import model_subreddit_topics

subreddits = ["ADHD"]
job_name = "ADHD_browsers_1"
query = "browser"
num_topics = 30
model_subreddit_topics.get_subreddit_topics(subreddits, query, job_name, num_topics)

# interface_query = "interface OR screen OR layout " \
#         "OR UI OR information overload OR " \
#         "reading text"




