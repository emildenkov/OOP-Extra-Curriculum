import time
import functools


def log_execution(label=None):

    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            display_name = label if label else func.__name__
            print(f"[START] {display_name}")
            result = func(*args, **kwargs)
            print(f"[ END ] {display_name}")
            return result
        return wrapper
    return outer


def timing(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIME ] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def validate_dataframe(func):

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        df = getattr(self, "data_frame", None)
        if df is None:
            raise RuntimeError(
                f"Cannot run '{func.__name__}': no data has been loaded yet. "
                f"Call load_data() first."
            )
        if len(df) == 0:
            raise RuntimeError(
                f"Cannot run '{func.__name__}': the loaded DataFrame is empty."
            )
        return func(self, *args, **kwargs)
    return wrapper