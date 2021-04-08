import json
import jwt

from mysetting       import secret, ALGORITHM
from accounts.models import Accounts

def loginauth(func):
    def wrapper(self, func, request):
        
        request_token = request.headers.get("token", None)
        print(request_token)
        
        request_id    = jwt.decode(request_token, secret['secret'], ALGORITHM).get('user_id')
        print(request_id)
        
        if Accounts.objects.filter(id = request_id).exist():
        
            request.user = Accounts.objects.get(id = request_id)
        
        return func(self, request)
    
    return wrapper
