import json

from django.views import View
from django.http  import JsonResponse

from .models import Img, Feed
from accounts.models import User

class FeedView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            img = data['img']
            username = data['username']
            contents = data['contents']
            title = data['title']

            if User.objects.filter(username=User.username).exists():
                Feed.objects.create(
                    img = img,
                    username = User.username,
                    contents = contents,
                    title = title
                    )
                return JsonResponse({'message': 'Upload Complete!'}, status = 200)
            else:
                return JsonResponse({'message' : 'Check your username'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'Keyerror occured!'}, status = 400)


        


