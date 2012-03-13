
class Config(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)

        return cls._instance


    def __init__(self):
        self.port = 9191
        self.addr = '127.0.0.1'
        self.auth_header = 'X-Authentication'
        self.auth_user_header = 'X-Authenticated-User'



