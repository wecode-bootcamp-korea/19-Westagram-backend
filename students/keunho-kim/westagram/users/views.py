import json
from django.http import JsonResponse
from django.views import View
from users.models import User


# Create your views here.

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_db = User.objects.all()

        try:
            if not data['id'] or not data['password']:
                return JsonResponse({'message': 'id & password are required'}, status=400)

            if user_db.filter(id=data['id']).exists():
                return JsonResponse({'message': 'id already exists!'}, status=400)

            elif user_db.filter(email=data['email']).exists():
                return JsonResponse({'message': 'email already exists!'}, status=400)

            elif user_db.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({'message': 'phone number already exists!'}, status=400)

            else:
                User.objects.create(id=data['id'], email=data['email'], phone_number=data['phone_number'])
                return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
