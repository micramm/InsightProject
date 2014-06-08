import os
import json

root_dir = 'yelp_data/html'

all_keys = [
            'address',
            'categories',
            'city',
            'country_code',
            'cross_streets',
            'deals',
            'display_address',
            'display_phone',
            'gift_certificates',
            'id',
            'image_url',
            'is_claimed',
            'is_closed',
            'menu_date_updated',
            'menu_provider',
            'mobile_url',
            'name',
            'neighborhoods',
            'phone',
            'postal_code',
            'rating',
            'rating_img_url',
            'rating_img_url_large',
            'rating_img_url_small',
            'review_count',
            'snippet_image_url',
            'snippet_text',
            'state_code',
            'url',
        ]

all_keys = set()

def flatten_dictionary(d, flattened = None):
    '''
    returns a single level representaion of a nexted dictionary
    '''
    if flattened is None:
        flattened = {}
    for key in d.keys():
        if not isinstance(d[key], dict):
            if not key in flattened:
                flattened[key] = d[key]
            else:
                raise Exception('Duplicate key')
        else:
            flatten_dictionary(d[key], flattened)
    return flattened

def html_to_csv():
    global all_keys
    file_counter = 0
    business_counter = 0
    for root, subFolders, files in os.walk(root_dir):
        for filename in files:
            path = os.path.join(root, filename)
            with open(path, 'r') as f:
                #converts the delimeters
                text = json.loads(f.read())
                #loads to dictionary
                text = json.loads(text)
    #             if file_counter == 0:
                businesses = text['businesses']
                for b in businesses:
                    b = flatten_dictionary(b)
#                     if business_counter == 0:
#                         for k, v in b.iteritems():
#                             print k, v
#                         first_keys = b.keys()
#                         first_keys = set(first_keys)
                    business_counter += 1
                    keys = b.keys()
                    keys = set(keys)
                    all_keys = all_keys.union(keys)
    #                 assert keys == first_keys, keys
    #                 print b.keys()
    #                 print type(text)
    #                 d = json.dumps(text)
    #                 print d
    #                 print text.dump()
    #             print f.read()
                file_counter += 1
    return file_counter, business_counter



# test = {'a': 1, 'b':2, 'c':{'ca': 3, 'cb': 4}, 'cb': 5}
# print flatten_dictionary(test)
    
    
file_counter, business_counter = html_to_csv()
print 'Finished processing {} files wiht {} businesses'.format(file_counter, business_counter)
for k in sorted(all_keys):
    print k
