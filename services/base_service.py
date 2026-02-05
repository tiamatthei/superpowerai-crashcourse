class BaseService:
    api_key: str
    api_secret: str
    email: str
    password: str

    def __init__(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

    def send_message(self, to, subject, body):
        pass
