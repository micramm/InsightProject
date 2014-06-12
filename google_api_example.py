from access_keys import access_keys

class google_api(object):
    
    def __init__(self):
        self.key = access_keys.google_key

    def generate_url(self, addresses):
        base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}W&destinations={1}&sensor=false&key={2}'
        rows = '|'.join(addresses)
        url = base_url.format(rows, rows, self.key)
        print url
    
api = google_api()
addresses = ['7 Avocet Dr. Redwood City, CA, 94065',
             '640 Masonic Way, Belmont, CA 94002',
             '716 Laurel St San Carlos, CA 94070',
             '796 Laurel St San Carlos, CA 94070',
             '260 Sheridan Ave, Palo Alto, CA',
             ]
api.generate_url(addresses * 2)