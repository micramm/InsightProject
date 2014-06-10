from mapquest_api import mapquest_api
import pandas as pd
import time 

mapquest = mapquest_api()
filename = 'location_frame_0.txt'
max_request = 100
df = pd.read_pickle(filename)
rows = df.shape[0]
iters = rows // max_request
#bounds for extracting data in chunks of length max_request
bounds = [(i * max_request, (i + 1) * max_request) for i in range(iters)]
#adding last section which may be smaller than max_request
bounds.append((iters * max_request, rows))

def lookup_addresses(address_list):
    lookup = mapquest.get_latlong(address_list)
    latitudes,longitudes,confidences = zip(*lookup)
    return latitudes, longitudes, confidences

##itearting over all bounds
def fill():
    for bound in bounds:
        print 'Working on bound: {}'.format(bound)
        addresses = df['complete_lookup_address'][bound[0]:bound[1]]
        latitudes,longitudes,confidences = lookup_addresses(addresses)
        df['latitude'][bound[0]:bound[1]] = latitudes
        df['longitude'][bound[0]:bound[1]] = longitudes
        df['latlng_confidence'][bound[0]:bound[1]] = confidences
        time.sleep(pd.np.random.rand())

def save():
    pd.to_pickle(df, filename)

fill()
save()