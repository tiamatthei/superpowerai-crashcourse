

class AuthenticationDependency:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
    
    def login(self):
        print(f"Logging in to {self.api_key} with API secret {self.api_secret}")
    
    def logout(self):
        print(f"Logging out from {self.api_key}")



