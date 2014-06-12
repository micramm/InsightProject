"""
High level routing functionality
"""
import sql_queries
import path_finder
import mapquest_api


class hopper(object):
    
    def _cumsum(self, iter, start = 1):
        """Cumulitve sum"""
        s = start
        yield s
        for elem in iter:
            s = s + elem
            yield s

    def __init__(self):
        self.db = sql_queries.sql()
        self.finder = path_finder.path_finder()
        self.distance_api = mapquest_api.mapquest_api()
        
    def get_path(self, start_lat, start_long, yelp_rating, categories):
        listings, lengths = self.db.get_listings(start_lat, start_long, yelp_rating, categories, number)
        coordinates = ['{0},{1}'.format(start_lat, start_long)]
        coordinates.extend('{0},{1}'.format(res[-2],res[-1]) for res in listings)
        sums = list(self._cumsum(lengths))
        common_groups = [range(sums[k], sums[k+1]) for k in range(len(sums) - 1)]
        distances = self.distance_api.get_all_to_all_matrix(coordinates)
        shortest_length, path = self.finder.get_fastest_path(distances, common_groups, start = 0, stop = 0)
        return [listings[p - 1] for p in path]

        
if __name__ == '__main__':
    hopper = hopper()
    start_lat,start_long = 37.524968,-122.2508315
    yelp_rating = 3.5
    categories = ['cafes','hair','grocery','lounges']
    number = 6
    path_list = hopper.get_path(start_lat, start_long, yelp_rating, categories)
    for p in path_list:
        print p[2]