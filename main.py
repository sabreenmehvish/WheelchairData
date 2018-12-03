import topics_rendering as visualizer
application = webapp2.WSGIApplication([ \
                                      ('/.*', MainHandler)
                                      ])


class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
        self.response.write(template.render(visualizer.generate_page(visualizer.csv_to_dict)))


