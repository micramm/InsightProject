"""
Class for finding the shortest path for a given matrix of distances between the points
"""
import itertools
import collections

class path_finder(object):
    
    #adapted from: http://stackoverflow.com/questions/11503065/python-function-to-flatten-generator-containing-another-generator
    def flatten(self, it):
        '''Iterator flattening  function'''
        for x in it:
            if (isinstance(x, collections.Iterable) and
                not isinstance(x, str) and not isinstance(x, tuple)):
                for y in self.flatten(x):
                    yield y
            else:
                yield x
    
    #from https://docs.python.org/2/library/itertools.html
    def pairwise(self, iterable):
        '''Function for generating pairways entries within an iterator'''
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return itertools.izip(a, b)
    
    def cost(self, distance_matrix, permutation, start, stop):
        """
        computes the cost of a given permutaiton of placed i.e (0,1,2,3,4) -> 1.0
        """
        pairs = self.pairwise(permutation)
        total = sum(distance_matrix[pair] for pair in pairs)
        #adding cost to get to the first point
        total+= distance_matrix[(start, permutation[0])]
        #adding cost to return from the last point
        total+= distance_matrix[(start, permutation[-1])]
        return total

    def get_fastest_path(self, distance_matrix, place_lists, start, stop):
        """
        cycles over all possible combination of places, where each place is picked
        from the correspodning group
        """
        selected_places = (itertools.product(*place_lists))
        #for each combination of places, consider all of the permutations of their order
        permuations = (itertools.permutations(places) for places in selected_places)
        #flatten generator of generators
        permuations = self.flatten(permuations)
        costs = (self.cost(distance_matrix, perm, start, stop) for perm in permuations)
        return min(zip(costs,permuations))
    
if __name__ == '__main__':
    import numpy as np
    import time
    distance_matrix = np.random.random((25,25))
    finder = path_finder()
    A = range(1, 6)
    B = range(6, 11)
    C = range(11, 16)
    D = range(16, 24)
    place_lists = [A, B, C, D]
    t1 = time.time()
    paths = finder.get_fastest_path(distance_matrix, place_lists, start = 0, stop = 0)
    print time.time() - t1
    print paths