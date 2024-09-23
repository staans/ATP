import decorators as dec

import time
import sys
import io

def while_functional_test():
    a = []
    @dec.while_functional
    def test():
        a.append(1)
    
    try:
        test()
    except RecursionError:
        assert len(a) == 997 # the amount of times the function can be called without error IF while_functional_test was called from global scope


def timed_cache_test():
    @dec.timed_cache(.05)
    def test():
        return time.perf_counter()

    start = time.perf_counter()
    values = set()
    while (time.perf_counter() < start+1):
        values.add(test())

    assert len(values) == 20, "timed_cache should've given back 20 unique value in a second with a timeout of .5, but didn;t"


def log_test():
    @dec.log
    def test1():
        pass

    @dec.log
    def test2():
        pass

    initial_stdout = sys.stdout
    sys.stdout = outputio = io.StringIO()
    
    test1()
    test2()

    sys.stdout = initial_stdout
    output = outputio.getvalue()
    outputio.close()

    assert (input(output + '\nDoes this look like correct logs for calling the local functions test1 and test2 in log_test? yes/anythin else\n') == 'yes'), "you said so" * 10000


def functional_unit_test_test():
    try:
        @dec.functional_unit_test(
            [
                ((1, 2), {}, 3),
                ((4, 2, lambda a, b: a*b), {}, 8),
                (([1,2,3], 1), {'op':lambda a, b: a[b]}, 2)
            ]
        )
        def bin_op(a, b, op=lambda a, b: a+b):
            return op(a, b)
    except:
        raise "functional_unit_test_test says thing is bad but isn't"

    try:
        @dec.functional_unit_test(
            [
                ((1, 2), {}, 4),
                ((4, 2, lambda a, b: a*b), {}, 7),
                (([1,2,3], 1), {'op':lambda a, b: a[b]}, -1)
            ]
        )
        def bin_op(a, b, op=lambda a, b: a+b):
            return op(a, b)
    except AssertionError:
        return
    raise "functional_unit_test_test doesn't raise but isn't good"

while_functional_test()
timed_cache_test()
log_test()
functional_unit_test_test()
print("all tests the good went")