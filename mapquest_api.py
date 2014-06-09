from access_keys import access_keys
import urllib
import urllib2
import json

class mapquest_api(object):
    
    def __init__(self):
        self.api_key = access_keys.mapquest_key
        
    def geocoding_url(self, locations):
        base_url = 'http://www.mapquestapi.com/geocoding/v1/batch?'
        encoding =  []
        for loc in locations:
            encoding.append(('location',loc))
        url = base_url + 'key={}&'.format(self.api_key) + urllib.urlencode(encoding)
        return url
    
    def geocoding_information(self, locations):
        url = self.geocoding_url(locations)
        try:
            conn = urllib2.urlopen(url, None)
            try:
                response = json.loads(conn.read())
            finally:
                conn.close()
        except urllib2.HTTPError, error:
                response = json.loads(error.read())    
        return response
    
    def get_latlong(self, locations):
        answer = []
        response = self.geocoding_information(locations)
        query_results = response['results']
        for res in query_results:
            #taking the first location as that's the most likely
            location = res['locations'][0]
            latlng = location['latLng']
            answer.append((latlng['lat'], latlng['lng'], location['geocodeQualityCode']))
        return answer