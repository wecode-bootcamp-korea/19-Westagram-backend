import json
from django.http  import JsonResponse

from django.views import View
from user.models  import User

class SignupView(View):
    def post(self, request):
        length_password = 8
        try:
            data = json.loads(request.body)
            if '@' and '.' not in data['email']:
                return JsonResponse({'MESSGAGE': 'INVALID EMAIL'}, status=400)
            if User.objects.filter(email= data['email']).exists():
                return JsonResponse({'MESSGAGE': 'ALREADY USED'}, status=400)
            if len(data['password']) <= length_password:
                return JsonResponse({'MESSGAGE': 'INVALID PASSWORD'}, status=400)
            user = User.objects.create(
                email        = data['email'],
                password     = data['password'],
                name         = data['name'],
                phone_number = data['phone_number']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=400)
