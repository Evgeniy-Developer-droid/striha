import json
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from user.models import User, Notification


@csrf_exempt
def read_notifications(request):
    data = json.loads(request.body)
    instances = Notification.objects.filter(target=request.user, key__in=data['keys'])
    instances.update(viewed=True)
    return JsonResponse({"message": "success"})


def get_all_notification(request):
    instances = Notification.objects.filter(target=request.user).order_by('-created')
    data = [{"key": item.key, 
             "title": item.title,
             "body": item.body,
             }
             for item in instances]
    return JsonResponse(data, safe=False)


def get_new_notification(request):
    instances = Notification.objects.filter(target=request.user, viewed=False).order_by('-created')[:3]
    data = [{"key": item.key, 
             "title": item.title,
             "body": item.body,
             }
             for item in instances]
    return JsonResponse(data, safe=False)


@csrf_exempt
def change_avatar(request):
    user = User.objects.get(pk=request.user.pk)
    user.avatar = request.FILES['avatar']
    user.save()
    return JsonResponse({
        "avatar": user.avatar.url
    })
