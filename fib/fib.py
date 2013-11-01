"""Sum nth fibonacci number"""
def fib(n):
    """Calculate nth fibonacci number 
       - from Haskell Wiki"""
    a, b = 0, 1
    for _ in xrange(n):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    import sys
    n = int(sys.argv[1])
    print sum(map(fib, xrange(n)))
