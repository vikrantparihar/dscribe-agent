from tenacity import retry

@retry(stop=3)
def safe_call(func, *args):

    return func(*args)