# import json
# import jwt

# from mysetting       import secret, ALGORITHM
# from accounts.models import Accounts

# def loginauth(func):
#     def wrapper(self, func, request):
        
#         data = json.loads(request.body)
#         print(data)
        
#         request_token = data.get("token", None)
#         request_id    = jwt.decode(request_token, secret['secret'], ALGORITHM).get('user_id')
#         print(request_token, request_id)
        
#         if Accounts.objects.filter(id = request_id).exist():
        
#             data['user'] = Accounts.objects.get(id = request_id)
#             print(data)
#         return func(self, data)
    
#     return wrapper