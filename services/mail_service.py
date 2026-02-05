from base_service import BaseService
from authentication_dependency import AuthenticationDependency

class MailService(BaseService, AuthenticationDependency):
    email: str
    password: str
    
    def __init__(self, email, password):
        super().__init__(email, password)
        
