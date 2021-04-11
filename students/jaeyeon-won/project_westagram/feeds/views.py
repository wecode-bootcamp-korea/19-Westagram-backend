import json

from django.views import View
from django.http  import JsonResponse

from .models import Feed
from accounts.models import User
from feeds.util import login_check



class FeedView(View):
    @login_check
    def post(self,request):
        data = json.loads(request.body)
    #    try:
        user = request.user

        if User.objects.filter(id=user.id).exists():
                Feed.objects.create(
                    contents= data['contents'],
                    title = data['title'],
                    img = data['img'],
                    username_id = request.user.id
                )
                return JsonResponse({'message': 'Upload Complete!'}, status = 200)
        else:
            return JsonResponse({'message' : 'Check your username'}, status = 400)
    #    except KeyError:
   #         return JsonResponse({'message': 'Keyerror occured!'}, status = 400

class PostView(View):
    @login_check
    def get(self, request):
        user = request.user
        feeds = Feed.objects.filter(username_id=user.id)
        feeds_list = []            
        for i in feeds:
            feeds_list.append(
                {
                #'user_name' : request.user.username,
                'username'  : User.objects.get(id=i.username_id).username,
                'image_url' : i.img,
                'content'   : i.contents,
                'created_at': i.created_at
                }
                    ) 
            return JsonResponse({'feeds': feeds_list}, status=200)
            

            