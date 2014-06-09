from mapquest_api import mapquest_api
import pandas as pd

filename = 'location_frame_0.txt'
max_request = 100

df = pd.read_pickle(filename)
print df.iloc[0].latitude
df['latitude'][0:2] = [0,1]
print df.iloc[0:3].latitude
#     print row

mapquest = mapquest_api()




locations = ['7 Avocet Drive, 94065', '260 Sheridan Ave, 94306']


# print mapquest.get_latlong(locations)