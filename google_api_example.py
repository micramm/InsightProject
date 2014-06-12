from access_keys import access_keys
import requests

class google_api(object):
    
    def __init__(self):
        self.key = access_keys.google_key

    def generate_url(self, addresses):
        base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}W&destinations={1}&sensor=false&key={2}'
        rows = '|'.join(addresses)
        url = base_url.format(rows, rows, self.key)
        return url
        
    def get_distance_matrix(self, addresses):
        url = self.generate_url(addresses)
        resp = requests.get(url)
        return resp.text
    
api = google_api()
addresses =     ['37.524968,-122.2508315',
                 '37.520515,-122.257320',
                 '37.494497,-122.246788',
                 '37.563856,-122.249911',
                 '37.487424,-122.235715',
                 '37.547685,-122.298318',
                 '37.551216,-122.301655',
                 '37.524105,-122.252680',
                 '37.519722,-122.275186',
                 '37.545468,-122.272053',]
#                  '37.529040,-122.289248',
#                  '37.561070 -122.274370',
#                  '37.568597 -122.266075',
#              ]
# print len(addresses)
import time
t1 = time.time()
text = api.get_distance_matrix(addresses)
# print text
print time.time() - t1