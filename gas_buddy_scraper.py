import requests
from pattern import web
import time
import os

download_delay = 0

information_url = 'http://www.sanfrangasprices.com/GasPriceSearch.aspx?typ=adv&fuel=A&srch=0&area=All%20Areas'

html = requests.get(information_url).text
dom = web.Element(html)

#get a list of all station brands
gas_stations = set()
for element in dom.by_tag('td'):
    table = element.by_id('ctl00_Content_P_PSC1_lstStations')
    if table:
        for entry in table.by_tag('option'):
            gas_stations.add(entry.content)
        break
gas_stations = gas_stations - set([u'All Stations'])
#get a list of all areas:
areas = set()
for element in dom.by_tag('td'):
    table = element.by_id('ctl00_Content_P_PSC1_lstAreas')
    if table:
        for entry in table.by_tag('option'):
            areas.add(entry.content)
        break
areas = areas - set([u'All Areas'])
#download all of the html
base_download_url = 'http://www.sanfrangasprices.com/GasPriceSearch.aspx?typ=adv&fuel=A&srch=0&area={0}&site=SanFran&station={1}&tme_limit=36'

dir_append = time.strftime('%b-%d-%Y-%H-%M-%S', time.localtime())
directory = 'gas_buddy_data/html/{}'.format(dir_append)
os.mkdir(directory)
os.chdir(directory)
for area in areas:
    for gas_station in gas_stations:
        print 'Download: {}, {}'.format(area, gas_station)
        download_url =  base_download_url.format(area, gas_station)
        html = requests.get(information_url).text
        current_file = open("{}-{}.html".format(area, gas_station),"w")
        current_file.write(html)
        current_file.close()
        time.sleep(download_delay)