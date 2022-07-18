
from operator import add


def something(function):
    def something2(x):
        def something3(y):

            return function(x, y)
        return something3
    return something2


print(something(add)(1)(2))
