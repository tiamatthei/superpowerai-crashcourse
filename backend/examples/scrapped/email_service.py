from base_service import BaseService


class EmailService(BaseService):
    email: str
    password: str
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

        
    def login(self):
        print(f"Logging in to {self.email} with password {self.password}")
        
        
    def send_email(self, to, subject, body):
        print(f"Sending email to {to} with subject {subject} and body {body}")


    def logout(self):
        print(f"Logging out from {self.email}")
