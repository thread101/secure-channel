

def handle_error(func):
    def wrapper(*args, **kwags):
        try:
            r = func(*args, **kwags)
        
        except Exception as e:
            r = f"[error] {e}"

        return r
    return wrapper

