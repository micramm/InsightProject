import json
import oauth2
import urllib
import urllib2
from access_keys import access_keys

consumer_key = access_keys.yelp_consumer_key
consumer_secret = access_keys.yelp_consumer_secret
token = access_keys.yelp_token
token_secret = access_keys.yelp_token_secret

def process_request(offset, category, bounds='37.9736,-122.5311|37.3333,-121.9000'):
    url_params = {}
    url_params['bounds'] = bounds 
    url_params['offset'] = offset
    url_params['category_filter'] = 'drugstores'
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

#banks
#drugstores
#postoffices
#restaurants
#food

response = process_request(0, 'banks')
print json.dumps(response, sort_keys=True, indent = 4)
# print response['businesses'][0].keys()

try:
    names = []
    for b in response['businesses']:
        names.append(b['name'])
#         print b['rating']
        print b['display_address']
    print len(response['businesses'])
    print sorted(names)
except Exception as e:
    print response
