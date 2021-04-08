import json
import jwt

from mysetting       import secret, ALGORITHM
from accounts.models import Accounts

def loginauth():
    def wrapper(self, func, request):
        
        request_token = request.headers.get("token", None)
        request_id    = jwt.decode(request_token, secret['secret'], ALGORITHM).get('user_id')
        user_id       = request.get('user_id')
        
        if Accounts.objects.get(id = request_id) == user_id:
        
            request.user = Accounts.objects.filter(id = user_id).first()
        
        return func(self, request)
    
    return wrapper
