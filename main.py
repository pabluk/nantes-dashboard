import os
import json
import jinja2
import webapp2
from google.appengine.api import memcache

from nantes_transport import BiclooStation, TANStation
from nantes_transport import InfoTrafic, OuestFrance


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class BiclooStationJSON(webapp2.RequestHandler):
    def get(self):
        station = {}

        id = self.request.get('id')
        name = self.request.get('name')
        if id and name:
            key_station = u'bicloo:%s:%s' % (id, name)
            station = memcache.get(key_station)
            if station is None:
                station = BiclooStation(id, name)
                memcache.add(key_station, station, 60)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(station.__dict__))


class TANStationJSON(webapp2.RequestHandler):
    def get(self):
        station = {}

        code = self.request.get('code')
        direction = self.request.get('direction')
        if code and direction:
            key_station = u'tan:%s:%s' % (code, direction)
            station = memcache.get(key_station)
            if station is None:
                station = TANStation(code, direction)
                memcache.add(key_station, station, 60)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(station.__dict__))


class NewsJSON(webapp2.RequestHandler):
    def get(self):
        messages = []

        key_news = u'infotrafic'
        messages_infotrafic = memcache.get(key_news)
        if messages_infotrafic is None:
            infotrafic = InfoTrafic(only_lines=['1', '2', '3'])
            messages_infotrafic = infotrafic.messages
            memcache.add(key_news, messages_infotrafic, 60 * 5)
        messages.extend(messages_infotrafic)

        key_news = u'ouestfrance'
        messages_ouestfrance = memcache.get(key_news)
        if messages_ouestfrance is None:
            ouestfrance = OuestFrance()
            messages_ouestfrance = ouestfrance.messages
            memcache.add(key_news, messages_ouestfrance, 60 * 5)
        messages.extend(messages_ouestfrance)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(messages))


app = webapp2.WSGIApplication([
                                ('/', MainPage),
                                ('/bicloo', BiclooStationJSON),
                                ('/tan', TANStationJSON),
                                ('/news', NewsJSON),
                              ], debug=True)
