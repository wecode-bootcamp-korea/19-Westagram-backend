import json
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from .models            import User, Following
from .validators        import email_validator, password_validator, phone_validator
from westagram.settings import SECRET_KEY, ALGORITHM
from .utils             import login_decorator

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            profile_img  = data.get('profile_img', 'https://exoffender.org/wp-content/uploads/2016/09/empty-profile.png')

            if not email_validator(email):
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400) 

            if not password_validator(password):
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)

            if not phone_validator(phone_number):
                return JsonResponse({'MESSAGE' : 'INVALID PHONE NUMBER'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL ALREADY EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email        = email,
                password     = hashed_password,
                name         = name,
                phone_number = phone_number,
                profile_img  = profile_img
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            print(request.body)
            data = json.loads(request.body)

            account  = data['account']
            password = data['password']
            user     = User.objects.filter(Q(email        = account) | 
                                           Q(phone_number = account) | 
                                           Q(name         = account)).first()

            if not user:
                return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=404)
            
            input_password = password.encode('utf-8')
            db_password    = user.password.encode('utf-8')

            if bcrypt.checkpw(input_password, db_password):
                token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'MESSAGE' : 'SUCCESS', 'token' : token}, status=200)

            return JsonResponse({'MESSAGE' : 'WRONG PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

class FollowView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']
            user    = request.user

            if not User.objects.filter(id = user_id).exists():
                return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=404)

            Following.objects.create(follow = user, followee_id = user_id)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)