from base_service import BaseService


class SmsService(BaseService):
    phone_number: str
    api_key: str
    
    def __init__(self, phone_number, api_key):
        self.phone_number = phone_number
        self.api_key = api_key

        
    def login(self):
        print(f"Logging in to {self.phone_number} with API key {self.api_key}")
        
        
    def send_sms(self, to, message):
        print(f"Sending SMS to {to} with message {message}")


    def logout(self):
        print(f"Logging out from {self.phone_number}")








