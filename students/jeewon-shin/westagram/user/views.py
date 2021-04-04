import json
from django.http  import JsonResponse

from django.views import View
from user.models  import User

class UserView(View):
    def post(self, request):
        data  = json.loads(request.body)
        users = User.objects.all()
        for user in users:
            user_email= user.email

        if data['email'] == '' or data['password'] == '':
            return JsonResponse({'MESSGAGE': 'KEY_ERROR'}, status=400)
        elif '@' and '.' not in data['email']:
            return JsonResponse({'MESSGAGE': 'This is not valid email.'}, status=400)
        elif data['email'] in user_email:
            return JsonResponse({'MESSGAGE': 'This email is already used.'}, status=400)
        elif len(data['password']) <= 8:
            return JsonResponse({'MESSGAGE': 'This is not valid password.'}, status=400)
        else:
            user = User.objects.create(
                email    = data['email'],
                password = data['password'],
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
