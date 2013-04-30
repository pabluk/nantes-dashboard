#!/usr/bin/env python
import json
import urllib
import urllib2
import xml.dom.minidom


class TANStation(object):
    _URL_ENDPOINT = "https://open.tan.fr/ewp/tempsattente.json/%s"

    def __init__(self, code, direction):
        self.code = code
        self.direction = direction
        self.slots = self._get_data()

    def _get_data(self):
        request = urllib2.Request(self._URL_ENDPOINT % self.code)
        f = urllib2.urlopen(request)
        json_response = f.read()
        data = json.loads(json_response)
        slots = []
        for item in data:
            if item['sens'] == int(self.direction):
                slot = {
                    'terminal': item['terminus'],
                    'time': item['temps'],
                }
                slots.append(slot)
        return slots

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
