import inspect
from functools import wraps

deferred = object()

# An implementation of the deferrable args wrapper suggested by Jonathon Fine


def deferrable_args(func):
    """
    Use this to decorate a function that you want to accept "defer" arguments, which will be overwritten by defaults.
    :param func: A function
    :return: A function with the same signature, which will swaps in defaults for deferred arguments then calls func
    """

    sig = inspect.signature(func)

    @wraps(func)
    def defer_args(*args, **kwargs):

        overridden_args = sig.bind(*args, **kwargs).arguments
        for k, v in overridden_args.items():
            if v is deferred:
                overridden_args[k] = sig.parameters[k].default

        return func(**overridden_args)

    return defer_args
