import json

from django.http    import JsonResponse
from django.views   import View

from .models        import User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            MINIMUM_PASSWORD_LENGTH = 8

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATED EMAIL'}, status=400)
        
            if User.objects.filter(phone_num=data['phone_num']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATED PHONE_NUM'}, status=400)
            
            if User.objects.filter(user_name=data['user_name']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATED USER_NAME'}, status=400)

            User.objects.create(
                    user_name   = data['user_name'],
                    phone_num   = data['phone_num'],
                    password    = data['password'],
                    email       = data['email']
            )
        
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)
