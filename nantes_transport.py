#!/usr/bin/env python
import re
import json
import urllib
import urllib2
import xml.dom.minidom
import feedparser


class TANStation(object):
    _URL_ENDPOINT = "https://open.tan.fr/ewp/tempsattente.json/%s"

    def __init__(self, code, direction):
        self.code = code
        self.direction = direction
        self.slots = self._get_data()

    def _get_data(self):
        request = urllib2.Request(self._URL_ENDPOINT % self.code)
        request.add_header('Accept-language', 'fr_FR')
        f = urllib2.urlopen(request)
        json_response = f.read()
        data = json.loads(json_response)
        slots = []
        for item in data:
            if item['sens'] == int(self.direction):
                slot = {
                    'terminal': item['terminus'],
                    'time': item['temps'],
                    'infotrafic': item['infotrafic'],
                }
                slots.append(slot)
        return slots

    def __repr__(self):
        return "%s" % self.__dict__


class InfoTrafic(object):
    _APP_KEY = 'PCHAJB5HPICTLFU'
    _URL_ENDPOINT = "http://data.nantes.fr/api/getInfoTraficTANTempsReel/1.0/%s/?output=json" % _APP_KEY

    def __init__(self, only_lines=[]):
        self.source = u'TAN Info Trafic'
        self.only_lines = only_lines
        self.messages = self._get_data()

    def _get_data(self):
        messages = []
        request = urllib2.Request(self._URL_ENDPOINT)
        f = urllib2.urlopen(request)
        json_response = f.read()
        data = json.loads(json_response)
        infotrafic_list = data['opendata']['answer']['data']['ROOT']['LISTE_INFOTRAFICS']['INFOTRAFIC']
        for item in  infotrafic_list:
            if not self.only_lines:
                messages.append({'message': item['INTITULE'], 'source': self.source})
                continue
            lines = item['TRONCONS'].split(';')
            for line_data in lines:
                line = re.search('\[(\w+)\/', line_data).group(1)
                if line in self.only_lines:
                    messages.append({'message': item['INTITULE'], 'source': self.source})
        return messages


    def __repr__(self):
        return "%s" % self.__dict__


class OuestFrance(object):
    _FEED_URL = "http://www.ouest-france.fr/dma-rss_-Toutes-les-DMA-redac-RSS_40771--pere-redac--44109_filDMA.Htm"

    def __init__(self):
        self.source = u'Ouest France'
        self.messages = self._get_data()

    def _get_data(self):
        messages = []
        feed = feedparser.parse(self._FEED_URL)
        for e in feed.entries[:40]:
            messages.append({'message': e.title, 'source': self.source})
        return messages


    def __repr__(self):
        return "%s" % self.__dict__


class BiclooStation(object):
    _URL_ENDPOINT = "http://www.bicloo.nantesmetropole.fr" \
                    "/service/stationdetails/nantes/%s"

    def __init__(self, id, name):
        self.id = id
        self.name = name

        dom = self._get_dom()
        self.available = self._get_available(dom)
        self.free = self._get_free(dom)
        self.total = self._get_total(dom)

    def __repr__(self):
        return "%s" % self.__dict__

    def _get_value(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return int(''.join(rc))

    def _get_available(self, dom):
        node = dom.getElementsByTagName("available")[0]
        return self._get_value(node.childNodes)

    def _get_free(self, dom):
        node = dom.getElementsByTagName("free")[0]
        return self._get_value(node.childNodes)

    def _get_total(self, dom):
        node = dom.getElementsByTagName("total")[0]
        return self._get_value(node.childNodes)

    def _get_dom(self):
        datasource = urllib.urlopen(self._URL_ENDPOINT % self.id)
        xml_content = datasource.read()
        return xml.dom.minidom.parseString(xml_content)


if __name__ == "__main__":
    print BiclooStation('18', u'PLACE VIARME')
    print TANStation('VIAR', 2)
    print InfoTrafic()
    print OuestFrance()
