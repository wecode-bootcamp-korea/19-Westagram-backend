import json
import datetime

from django.utils     import timezone
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count, F
# from django.core      import serializers

from users.utils      import login_decorator

from .models          import Feed, Tag, Media, Comment
from users.models     import User


class IndexView(View):
    @login_decorator
    def get(self, request):
        try:
            user        = request.user
            my_followee = user.follow.all()

            feeds = list(
                user
                    .feed_set
                    .filter(
                        created_at__gte=timezone.now() - datetime.timedelta(days=1)
                    )
                    .annotate(
                        author_name=F('author__name'),
                        likes=Count('feedlike')
                    )
            )

            for followee in my_followee:
                followee_id = followee.followee_id

                if User.objects.filter(id = followee_id).exists():
                    followee = User.objects.get(id = followee_id)

                    followee_feeds = list(
                        followee
                            .feed_set
                            .filter(
                                created_at__gte=timezone.now() - datetime.timedelta(days=1)
                            )
                            .annotate(
                                author_name=F('author__name'),
                                likes=Count('feedlike')
                            )
                    )

                    feeds += followee_feeds

            result = []

            for feed in feeds:
                feed_info = {
                    'feed_id': feed.id,
                    'author_name': feed.author.name,
                    'author_profile_image': feed.author.profile_img,
                    'text': feed.text,
                    'created_at': feed.created_at,
                    'urls': list(feed.media_set.values_list('url', flat=True)),
                    'comments': list(feed.comment_set.values_list('text', flat=True))
                }
                result.append(feed_info)

            return JsonResponse({'MESSAGE': 'SUCCESS', 'FEEDS': result}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)


class DetailView(View):
    @login_decorator
    def get(self, request, feed_id = None):
        try:
            print(feed_id)
            if not feed_id:
                return JsonResponse({'MESSAGE': 'INVALID FEED'}, status=404)

            user = request.user

            feed = Feed.objects.filter(id = feed_id) \
                               .annotate(
                                   author_name=F('author__name'),
                                   likes = Count('feedlike')
                                ) \
                                .first()

            feed_info = {
                'feed_id' : feed.id,
                'author_name' : feed.author.name,
                'author_profile_image' : feed.author.profile_img,
                'text' : feed.text,
                'created_at' : feed.created_at,
                'urls' : list(feed.media_set.values_list('url', flat=True)),
                'comments' : list(feed.comment_set.values_list('text', flat=True))
            }

            return JsonResponse({'MESSAGE': 'SUCCESS', 'FEED': feed_info}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

class FeedView(View):
    @login_decorator
    def post(self, request):
        try:
            data  = json.loads(request.body)
            media = data['media']
            tags  = data['tags']
            text  = data['text']
            user  = request.user

            feed = Feed(
                author = user,
                text   = text
            )

            feed.save()

            media_objects = [ Media(feed = feed, url = url) for url in media ]
            Media.objects.bulk_create(media_objects)

            tag_objects = [ Tag(name = name) for name in tags ]

            for tag in tag_objects:
                tag.save()
                feed.tag.add(tag)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

class LikeView(View):
    @login_decorator
    def post(self, request, content_id = None, content = None):
        try:
            user = request.user
            
            if not content_id or not content:
                return JsonResponse({'MESSAGE' : 'INVALID PAGE'}, status=404)

            if content == 'comment' and Comment.objects.filter(pk = content_id).exists:
                target = Comment.objects.get(pk = content_id)
            elif content == 'feed' and Feed.objects.filter(pk = content_id).exists():
                target = Feed.objects.get(pk = content_id)
            else:
                return JsonResponse({'MESSAGE' : 'INVALID PAGE'}, status=404)

            if not target.like.filter(id = user.id).exists:
                target.like.add(user)
            else:
                target.like.remove(user)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

class CommentView(View):
    @login_decorator
    def post(self, request, feed_id):
        try:
            if not feed_id:
                return JsonResponse({'MESSAGE' : 'INVALID PAGE'}, status=404)

            user    = request.user
            author  = user
            data    = json.loads(request.body)
            text    = data['text']

            if not Feed.objects.filter(id = feed_id).exists():
                return JsonResponse({'MESSAGE': 'INVALID FEED'}, status=404)

            Comment.objects.create(author = author, feed_id = feed_id, text = text)
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            pass #TODO
        except:
            pass #TODO