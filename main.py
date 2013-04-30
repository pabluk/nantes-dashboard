import os
import jinja2
import webapp2
from nantes_transport import BiclooStation, TANStation


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):

    def get(self):
        bicloo_stations = [
            BiclooStation('18', u'PLACE VIARME'.title()),
            BiclooStation('17', u'SAINTE ELISABTEH'.title()),
        ]

        tan_station = TANStation('VIAR', 2)

        template_values = {
            'bicloo_stations': bicloo_stations,
            'tan_station': tan_station,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
