import json
import re

from django.views import View
from django.http  import JsonResponse

from user.models  import User

class SignUpView(View):
    def post(self, request):
        data                 = json.loads(request.body)
        identification_check = re.compile('[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_check       = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

        try:
            if User.objects.filter(identification=data['identification']):
                return JsonResponse({'MESSAGE':'IDENTIFICATION_ALREADY_EXIST'}, status=400)
            elif User.objects.filter(nickname=data['nickname']):
                return JsonResponse({'MESSAGE':'NICKNAME_ALREADY_EXIST'}, status=400)
            elif not identification_check.match(data['identification']):
                return JsonResponse({'MESSAGE':'IDENTIFICATION IS NOT VALID'}, status=400)
            elif not password_check.match(data['password']):
                return JsonResponse({'MESSAGE':'PASSWORD IS NOT VALID'}, status=400)
            else:
                User.objects.create(
                    identification = data['identification'],
                    password       = data['password'],
                    name           = data['name'],
                    nickname       = data['nickname']
                )

                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)






