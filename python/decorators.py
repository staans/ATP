import time

# repeat the given function forever (or until python complains)
def while_functional(func : callable):
    def r(*args : list[any], **kwargs : dict[any, any]):
        func(*args, **kwargs)
        r(*args, **kwargs)
    return r

# cache the function's output for the given amount of time
def timed_cache(timeout_seconds : float):
    def decorator(func : callable):
        prev_value = None
        prev_time = float('-inf')

        def r(*args : list[any], **kwargs : dict[any, any]):
            nonlocal prev_time, prev_value
            cur_time = time.perf_counter()
            if (cur_time > prev_time+timeout_seconds):
                prev_time = cur_time
                prev_value = func(*args, **kwargs)
            return prev_value
    
        return r

    return decorator

# log function calls
def log(func : callable):
    def r(*args : list[any], **kwargs : dict[any, any]):
        print(f"Function {str(func)} called with arguments {args} and keyword arguments {kwargs}")
        func(*args, **kwargs)
    return r

# automatically test the function against a given set of expected return values for sets of arguments
def functional_unit_test(test_values : list[tuple[list, dict, any]]):
    def decorator(func : callable):
        for (args, kwargs, expected) in test_values:
            got = func(*args, **kwargs)
            assert got == expected, f"Function {str(func)} failed test - Returned {got} but expected {expected} with args {args} and kwargs {kwargs}."

        return func
    
    return decorator