import json
import oauth2
import urllib
import urllib2
from access_keys import access_keys
import os
import time

consumer_key = access_keys.yelp_consumer_key
consumer_secret = access_keys.yelp_consumer_secret
token = access_keys.yelp_token
token_secret = access_keys.yelp_token_secret

def process_request(offset, category, bounds='37.9736,-122.5311|37.3333,-121.9000'):
    url_params = {}
    url_params['bounds'] = bounds 
    url_params['offset'] = offset
    url_params['category_filter'] = category
    response = request('api.yelp.com','/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
    return response

def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
    """Returns response for API request."""
    # Unsigned URL
    encoded_params = ''
    if url_params:
        encoded_params = urllib.urlencode(url_params)
        url = 'http://%s%s?%s' % (host, path, encoded_params)
    # Sign the URL
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})
    token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    # Connect
    try:
        conn = urllib2.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
    except urllib2.HTTPError, error:
        response = json.loads(error.read())    
    return response

def get_total_result(category, bounds):
    '''
    returns the number of total results for the category inside bounds
    '''
    totals = []
    for bound in bounds:
        response = process_request(0, category, bound)
        totals.append(response['total'])
    print totals
    return max(totals)

def division_to_bounds(division, map_bounds):
    lat_start, lon_start, lat_stop, lon_stop = map_bounds
    delta = (lon_stop - lon_start) / division
    bound_form = '{:.4f},{:.4f}|{:.4f},{:.4f}'
    bounds = [bound_form.format(lat_start, lon_start + i * delta, lat_stop, lon_start + (i + 1) * delta) for i in range(division)]
    return bounds

def get_required_division(category, max_elements = 1000, map_bounds=(37.9736,-122.5311,37.3333,-121.9000)):
    '''
    returns the number of segments the latitude needs to be split into such that
    the number of businesses in every segment is below max_elements
    '''
    division = 1
    bounds = division_to_bounds(division, map_bounds)
    while get_total_result(category, bounds) > max_elements:
        division *= 2
        bounds = division_to_bounds(division, map_bounds)
    return division

def save_one_bound(category, bound, division_count):
    start = 0
    response = process_request(start, category, bound)
    result_count = len(response['businesses'])
    while result_count:
        text =  json.dumps(response, sort_keys=True)
        with open('data_{}_{}.txt'.format(division_count, start), 'w') as outfile:
            json.dump(text, outfile)
        start += 20
        response = process_request(start, category, bound)
        result_count = len(response['businesses'])
        
def save_all_bounds(category, required_divisions, map_bounds=(37.9736,-122.5311,37.3333,-121.9000)):
    dir_append = time.strftime('%b-%d-%Y-%H-%M-%S', time.localtime())
    directory = 'yelp_data/html/{}/{}'.format(category, dir_append)
    os.mkdir(directory)
    os.chdir(directory)
    bounds = division_to_bounds(required_divisions, map_bounds)
    for count, bound in enumerate(bounds):
        print 'saving division', count
        save_one_bound(category, bound, count)
    

# print get_required_division('beautysvc')

# save_all_bounds('banks', 2)
# save_all_bounds('drugstores', 1)
# save_all_bounds('postoffices', 1)
# save_all_bounds('restaurants', 128)
# save_all_bounds('food', 64)
# save_all_bounds('shopping', 256)
# save_all_bounds('nightlife', 16)
# save_all_bounds('localservices', 32)
# save_all_bounds('homeservices', 128)
# save_all_bounds('beautysvc', 64)

# response = process_request(0, 'banks')
# print json.dumps(response, sort_keys=True, indent = 4)
# # print response['businesses'][0].keys()
# 
# try:
#     names = []
#     for b in response['businesses']:
#         names.append(b['name'])
# #         print b['rating']
#         print b['display_address']
#     print len(response['businesses'])
#     print sorted(names)
# except Exception as e:
#     print response
