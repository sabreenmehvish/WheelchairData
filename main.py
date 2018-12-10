import model_subreddit_topics
import http.server as server
import socketserver
import cgi


class ModellingRequestHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        server.SimpleHTTPRequestHandler.do_GET(self)
        print("Got")

    def do_POST(self):
        print(self.requestline)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        sublist = form["subreddits"].value
        subreddits = [sub.strip() for sub in sublist.split(",")]
        print(subreddits)
        job_name = form["job_name"].value
        query = form["query"].value
        num_topics = int(form["num_topics"].value)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html_string = model_subreddit_topics.get_subreddit_topics(subreddits, query, job_name, num_topics)
        self.wfile.write(bytes(html_string, "UTF-8"))


def run(server_class=server.HTTPServer, handler_class=ModellingRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()






