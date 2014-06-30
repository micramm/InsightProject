from repoze.lru import lru_cache

class test_lru(object):
    
    def __init__(self):
        pass

    @lru_cache(maxsize=500)
    def fib(self, n):
        print 'computing', n
        return [[1],[2],['hello',1]]



if __name__ == '__main__':
    test = test_lru()
    print test.fib(10)
    print test.fib(10)