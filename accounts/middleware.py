class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, *args, **kwargs):
        response = self.get_response(*args, **kwargs)
        return response
