import os
import json
import csv

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

#test code for dictionary flatterning
# test = {'a': 1, 'b':2, 'c':{'ca': 3, 'cb': 4}, 'cb': 5}
# print flatten_dictionary(test)

def html_to_csv(all_keys, dict_writer):
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
                businesses = text['businesses']
                for b in businesses:
                    b = flatten_dictionary(b)
#                     print 'address' in b
                    business_counter += 1
                    keys = set(b.keys())
                    keys = set(keys)
                    assert keys.issubset(set(all_keys)), ("found unknown key: " + keys - set(all_keys))
                    dict_writer.writerow(b)
                file_counter += 1
                print file_counter
    return file_counter, business_counter

with open('yelp_data/yelp_raw_2.csv', 'w') as csv_file:
    dict_writer = csv.DictWriter(csv_file, all_keys)
    dict_writer.writer.writerow(all_keys)
    file_counter, business_counter = html_to_csv(all_keys, dict_writer)
print 'Finished processing {} files wiht {} businesses'.format(file_counter, business_counter)
