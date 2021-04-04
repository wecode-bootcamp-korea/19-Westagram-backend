import json
import re

from django.http    import JsonResponse
from django.views   import View

from .models        import Accounts

class SignupView(View):

    def post(self, request):
        data     = json.loads(request.body)
        accounts = Accounts.objects.all()
        
        vaildation = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        
        for account in accounts:
            if data['user_id'] == account.user_id:
                return JsonResponse({'message': 'KEY_ERROR ID already exist'}, status = 400)
        
        if '@' not in data['user_id'] or '.' not in data['user_id']:
            return JsonResponse({'message': 'KEY_ERROR Inappropriate ID'}, status = 400)
        # if .match(data['user_id']):
        elif len(data['user_pw']) < 8:
            return JsonResponse({'message': 'KEY_ERROR Password too short!'}, status = 400)

        elif len(data['user_phone']) < 10:
            return JsonResponse({'message': 'KEY_ERROR Wrong PHONE number'}, status = 400)

        else:
            Accounts.objects.create(user_id       = data['user_id'],
                                    user_pw       = data['user_pw'],
                                    user_name     = data["user_name"],
                                    user_phone    = data['user_phone'],
                                    user_nickname = data['user_nickname'])
            
            return JsonResponse({"message": "Sign up complete!"}, status = 201)

class LoginView(View):

    def post(self, request):
        data = json.loads(request.body)
        
        
    pass


