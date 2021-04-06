import json
import bcrypt

from django.http  import JsonResponse

from django.views import View
from user.models  import User

class SignupView(View):
    def post(self, request):
        PASSWORD_LENGTH = 8
        try:
            data = json.loads(request.body)
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            if '@' not in data['email']:
                return JsonResponse({'MESSGAGE': 'INVALID EMAIL'}, status=400)
            elif '.' not in data['email']:
                return JsonResponse({'MESSGAGE': 'INVALID EMAIL'}, status=400)

            if User.objects.filter(email= data['email']).exists():
                return JsonResponse({'MESSGAGE': 'ALREADY USED'}, status=400)

            if len(data['password']) <= PASSWORD_LENGTH:
                return JsonResponse({'MESSGAGE': 'INVALID PASSWORD'}, status=400)

            User.objects.create(
                email        = data['email'],
                password     = hashed_password,
                name         = data['name'],
                phone_number = data['phone_number']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=400)