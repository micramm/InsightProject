from access_keys import access_keys
import urllib
import urllib2
import json
import requests

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
    
    def distance_matrix_url(self):
        base_url = 'http://www.mapquestapi.com/directions/v2/routematrix?'
        url = base_url + 'key={}&'.format(self.api_key) + 'doReverseGeocode:false&'
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
    
    def get_all_to_all_matrix(self, locations):
        url = self.distance_matrix_url()
        
        content =  {'locations': locations,
                   'options': {
                               'allToAll': True
                                }
                   }
        resp = requests.post(url, data = json.dumps(content))
        return json.loads(resp.text)["distance"]

if __name__ == '__main__':
    api = mapquest_api()
    addresses = ['37.524968,-122.2508315',
                 '37.520515 -122.257320',
                 '37.494497 -122.246788',
                 '37.563856 -122.249911',
                 '37.487424 -122.235715',
                 '37.547685 -122.298318',
                 '37.551216 -122.301655',
                 '37.524105 -122.252680',
                 '37.519722 -122.275186',
                 '37.545468 -122.272053',
                 '37.529040 -122.289248',
                 '37.561070 -122.274370',
                 '37.568597 -122.266075',
             ]
    import time
    t = time.time()
    matrix = api.get_all_to_all_matrix(addresses)
    print time.time() - t
#     print matrix
    