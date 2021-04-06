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

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSGAGE': 'INVALID EMAIL'}, status=400)

            if User.objects.filter(email= data['email']).exists():
                return JsonResponse({'MESSGAGE': 'ALREADY USED'}, status=400)

            if User.objects.filter(user_name=data['user_name']).exists():
                return JsonResponse({'MESSGAGE': 'ALREADY USED'}, status=400)

            if len(data['password']) <= PASSWORD_LENGTH:
                return JsonResponse({'MESSGAGE': 'INVALID PASSWORD'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            decode_hash_pw = hashed_password.decode('utf-8')

            User.objects.create(
                email        = data['email'],
                nickname     = data['nickname'],
                name         = data['name'],
                phone_number = data['phone_number'],
                password     = decode_hash_pw
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=400)