from access_keys import access_keys

class four_square_api(object):
    
    def __init__(self, version_date = '20140603'):
        self.client_id = access_keys.four_square_client_id
        self.client_secret = access_keys.four_square_client_secret
        self.version_date = version_date
        
    def get_next_venues(self, venue_id):
        url = self.next_venue_url(venue_id)
        print url
        
    def next_venue_url(self, venue_id):
        base_url = 'https://api.foursquare.com/v2/venues/{0}/nextvenues?&client_id={1}&client_secret={2}&v={3}'
        base_url = base_url.format(venue_id, self.client_id, self.client_secret, self.version_date)
        return base_url
    
if __name__ == '__main__':
    #testing the api with a simple call
    api = four_square_api()
    venue_id = '40a55d80f964a52020f31ee3'
    url = api.get_next_venues(venue_id)

#mapquest, getting all gas stations
'''
http://www.mapquestapi.com/search/v2/radius?key=Fmjtd%7Cluur2g6rnh%2Crn%3Do5-9a8al6&callback=renderExampleOneResults&origin=redwood%20city,%20ca&hostedData=mqap.ntpois|group_sic_code=?|554101&radius=10&maxMatches=1000
http://www.mapquestapi.com/geocoding/v1/batch?key=Fmjtd%7Cluur2g6rnh%2Crn%3Do5-9a8al6&callback=renderBatch&location=7 Avocet Drive, 94065&location=1835 Delaware Street, 94703
http://www.mapquestapi.com/geocoding/v1/batch?key=Fmjtd%257Cluur2g6rnh%252Crn%253Do5-9a8al6

'''