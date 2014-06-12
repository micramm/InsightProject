"""
Class for performing queries on the mysql database
"""
import pymysql
from access_keys import access_keys

database_name = 'Insight' 

class sql(object):
    
    def __init__(self):
        conn = pymysql.connect(host='localhost', user='root')
#         conn = pymysql.connect(host='insight.clzrh9aax7lr.us-east-1.rds.amazonaws.com', user='michaelramm', passwd = access_keys.amazon_rds_password)
        self.cursor = conn.cursor()
        self.cursor.execute("""USE {};""".format(database_name))
        
    def _query_close_locations(self, latitde, longitude, yelp_rating):
        #returns the query to create the filtered_yelp table with locations close to the provided coordinates
        return """
CREATE OR REPLACE VIEW filtered_yelp AS
SELECT *, SQRT(POW((latitude - {0}),2) + POW((longitude - {1}),2)) as distance
FROM yelp
WHERE rating >= {2}""".format(latitde, longitude, yelp_rating)
    
    def _query_match_category(self, category):
        #creates a view  object for locations matching the provided category
        return """CREATE OR REPLACE VIEW cats AS
SELECT id, short_category
FROM categories
WHERE short_category = '{}'""".format(category)
    
    def _query_get_number(self, number = 6): 
        #selects places that are close enough (in the filtered_yelp table) and match category (in the cats) table
        return """
SELECT cats.id as id, short_category, display_address, image_url, phone, rating, rating_image_url_large, url, latitude, longitude 
FROM cats
JOIN filtered_yelp
ON cats.id = filtered_yelp.id
ORDER BY distance
LIMIT {}""".format(number)
    
    def get_listings(self, start_lat, start_long, yelp_rating, categories, number):
        """
        Returns the listings of locations closest to the specified location (start_lat, start_long)
        that belong to one of the categories. Number specifies the number of listings to return for
        each category
        """
        results = []
        lengths = []
        self.cursor.execute(self._query_close_locations(start_lat, start_long, yelp_rating))
        for category in categories:
            self.cursor.execute(self._query_match_category(category))
            self.cursor.execute(self._query_get_number(number))
            initial_length = len(results)
            results.extend(self.cursor.fetchall())
            final_length = len(results)
            lengths.append(final_length - initial_length)
        return results, lengths
    
if __name__ == '__main__':
    db = sql()
    start_lat = 37.524968
    start_long = -122.2508315
    yelp_rating = 3.5
    categories = ['cafes','hair','grocery','lounges']
    number = 6
    listings, groups = db.get_listings(start_lat, start_long, yelp_rating, categories, number)
    print groups
    print listings