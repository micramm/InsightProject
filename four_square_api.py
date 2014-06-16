from access_keys import access_keys
import requests
import json

class four_square_api(object):
    
    def __init__(self, version_date = '20140603'):
        self.client_id = access_keys.four_square_client_id
        self.client_secret = access_keys.four_square_client_secret
        self.version_date = version_date
        
    def next_venue_url(self, venue_id):
        base_url = 'https://api.foursquare.com/v2/venues/{0}/nextvenues?&client_id={1}&client_secret={2}&v={3}'
        base_url = base_url.format(venue_id, self.client_id, self.client_secret, self.version_date)
        return base_url
    
    def venue_explore_url(self):
        base_url = 'https://api.foursquare.com/v2/venues/explore?&client_id={0}&client_secret={1}&v={2}'
        base_url = base_url.format(self.client_id, self.client_secret, self.version_date)
        return base_url
    
    def venue_search_url(self):
        base_url = 'https://api.foursquare.com/v2/venues/search?&client_id={0}&client_secret={1}&v={2}&limit=50'
        base_url = base_url.format(self.client_id, self.client_secret, self.version_date)
        return base_url
    
    def venue_hours_url(self, venue_id):
        base_url = "https://api.foursquare.com/v2/venues/{0}/hours?&client_id={1}&client_secret={2}&v={3}"
        base_url = base_url.format(venue_id, self.client_id, self.client_secret, self.version_date)
        return base_url
    
    def find_matching_business(self, name, zip_code, matching_phone):
        '''
        returns the four square id of the matching business with the given name, zip and phone
        '''
        #perform the search by name and zip code, and then find the matching phone among the results
        url = self.venue_explore_url()
        url += '&query={0}&near={1}'.format(name, zip_code)
        response = requests.get(url)
        data = json.loads(response.text)
        response = data['response']
        listings = response['groups'][0]['items']
        #loop over the listings searching for the phone match
        for place in listings:
            venue = place['venue']
            ident = venue['id']
            exact_phone = venue['contact'].get('phone')
            if exact_phone is not None:
                if int(exact_phone) == matching_phone:
                    return ident
        return None
    
    def find_next_venues(self, from_venue_id):
        url = self.next_venue_url(from_venue_id)
        response = requests.get(url)
        data = json.loads(response.text)
        response = data['response']
        venues = response['nextVenues']['items']
        result = [(from_venue_id, venue['id'], venue['stats']['checkinsCount']) for venue in venues]
        return result

if __name__ == '__main__':
    #testing the api with a simple call
    api = four_square_api()
#     match = api.find_matching_business("Peet's", 94070, 6506050003)
    hours_url = api.venue_hours_url('40a55d80f964a52020f31ee3')
#     result = api.find_next_venues('49c445c0f964a520b6561fe3')
    print hours_url
#     print match
#     venue_id = '40a55d80f964a52020f31ee3'
#     venue_id = '49f78793f964a520b16c1fe3'#town
#     venue_id = '4abedc49f964a520509020e3'#piacere
#     venue_id = '4acd7b59f964a5202fcc20e3'#orchid room
#     venue_id = '4085b980f964a52091f21ee3'#san carlos club
#     venue_id = '4e7f455ed3e3b8285efe60fb'#peets coffee and tea
#     venue_id = '4ca4ecc897c8a1cde15662a5'#the office bar and grill
#    venue_id = '4a53b739f964a520a6b21fe3'#snakers
# '4aee20acf964a5205bd221e3' #the cask
# '4da2242fb1c937048088dea1' #seia sushi
#412a8500f964a520730c1fe3 #mcgraw
#49e81b21f964a52040651fe3 #o'neill
#     url = api.get_next_venues("4b22b4edf964a5202f4c24e3")
#     url = api.venue_explore_url()
#     url = api.venue_search_url()
#     print url