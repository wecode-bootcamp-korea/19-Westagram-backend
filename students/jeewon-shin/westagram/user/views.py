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

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSGAGE': 'ALREADY USED'}, status=400)

            if User.objects.filter(nickname=data['nickname']).exists():
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

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data.get('email')
            nickname = data.get('nickname')
            phone_number = data.get('phone_number')

            if email:
                if User.objects.filter(email=data['email']).exists():
                    passwords = User.objects.get(email=data['email']).password
                else:
                    return JsonResponse({'MESSAGE': 'NO VALIED'}, status=401)
            if nickname:
                if User.objects.filter(nickname=data['nickname']).exists():
                    passwords = User.objects.get(nickname=data['nickname']).password
                else:
                    return JsonResponse({'MESSAGE': 'NO VALIED'}, status=401)
            if phone_number:
                if User.objects.filter(phone_number=data['phone_number']).exists():
                    passwords = User.objects.get(phone_number=data['phone_number']).password
                else:
                    return JsonResponse({'MESSAGE': 'NO VALIED'}, status=401)

            bcrypt.checkpw(data['password'].encode('utf-8'),passwords.encode('utf-8'))
            return JsonResponse({'MESSGAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)



