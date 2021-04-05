import json
from django.http  import JsonResponse

from django.views import View
from user.models  import User

class SignupView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            if '@' and '.' not in data['email']:
                return JsonResponse({'MESSGAGE': 'This is not valid email.'}, status=400)
            elif User.objects.filter(email= data['email']).exists():
                return JsonResponse({'MESSGAGE': 'This email is already used.'}, status=400)
            elif len(data['password']) <= 8:
                return JsonResponse({'MESSGAGE': 'This is not valid password.'}, status=400)
            user = User.objects.create(
                email           = data['email'],
                password        = data['password'],
                name            = data['name'],
                phone_number    = data['phone_number']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=400)
