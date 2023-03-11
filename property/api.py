from django.http import HttpResponseBadRequest, JsonResponse, Http404
from .models import Contract, RealEstate, RealEstateMedia, RequestMedia, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict


@csrf_exempt
def payment_single_data(request):
    result = dict()
    mode = {
        "rent": "Місячна оплата", "internet": "Інтернет",
        "gas": "Газопостачання", "water": "Водопостачання",
        "electricity": "Електроенергія", "other": "Інше",
    }
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Auth")
    if request.user.role == 'landlord':
        instance = Transaction.objects.get(key=request.GET.get("key", "000"), landlord=request.user)
        result['avatar'] = instance.tenant.avatar.url if instance.tenant.avatar else "/static/assets/images/faces/face0.jpg"
        result['role'] = "Орендар"
        result['email'] = instance.tenant.email
        result['full_name'] = f'{instance.tenant.first_name} {instance.tenant.last_name}'
    else:
        instance = Transaction.objects.get(key=request.GET.get("key", "000"), tenant=request.user)
        result['avatar'] = instance.landlord.avatar.url if instance.landlord.avatar else "/static/assets/images/faces/face0.jpg"
        result['role'] = "Орендодавець"
        result['email'] = instance.landlord.email
        result['full_name'] = f'{instance.landlord.first_name} {instance.landlord.last_name}'
    result['amount'] = instance.amount
    result['card'] = instance.card_mask
    result['created'] = instance.created.strftime("%d/%m/%Y, %H:%M:%S")
    result['description'] = instance.description
    result['mode'] = mode.get(instance.mode, "Інше")

    if instance.sender_card_type == "visa":
        result['sender_card_type_svg'] = "/static/assets/images/visa-svgrepo-com.svg"
    else:
        result['sender_card_type_svg'] = "/static/assets/images/mastercard-svgrepo-com.svg"

    if instance.status == "success":
        result['status'] = "Успішно"
    elif instance.status == "failed":
        result['status'] = "Невдача"
    else:
        result['status'] = "Очікування"
    return JsonResponse(result)


@csrf_exempt
def request_media_upload(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Auth")
    instance = RequestMedia.objects.create(
        file=request.FILES['file']
    )
    return JsonResponse({
        "id": instance.pk,
        "file": instance.file.url
    })


@csrf_exempt
def delete_request_media(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Auth")
    pk = request.POST.get('id', 0)
    try:
        instance = RequestMedia.objects.get(pk=pk, request__isnull=True)
        instance.delete()
        return JsonResponse({"message": "Видаленно"})
    except RequestMedia.DoesNotExist:
        return HttpResponseBadRequest("Не")


@csrf_exempt
def get_contract_status_tenant(request):
    contract = Contract.objects.filter(tenant=request.user).exclude(status__in=["terminated"]).order_by('-created')
    if contract.exists():
        contract = contract.first()
        return JsonResponse({"status": contract.status})
    return JsonResponse({"status": "None"})


@csrf_exempt
def get_real_estate_by_token(request):
    try:
        instance = RealEstate.objects.get(share_token=request.POST.get("token", "empty"))

        media = list()
        media_instances = RealEstateMedia.objects.filter(real_estate=instance)
        for media_item in media_instances:
            media_dict = model_to_dict(media_item, fields=[field.name for field in media_item._meta.fields])
            media_dict['file'] = media_dict['file'].url
            media.append(media_dict)

        instance = model_to_dict(instance, fields=[field.name for field in instance._meta.fields])
        instance["media"] = media
        return JsonResponse(instance)
    except RealEstate.DoesNotExist:
        return JsonResponse({"error": "Нерухомість не знайдено. Невірний токен"})


@csrf_exempt
def delete_real_estate_media(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Auth")
    pk = request.POST.get('id', 0)
    try:
        instance = RealEstateMedia.objects.get(landlord=request.user, pk=pk)
        instance.delete()
        return JsonResponse({"message": "Видаленно"})
    except RealEstateMedia.DoesNotExist:
        return HttpResponseBadRequest("Не")


@csrf_exempt
def upload_real_estate_media(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Auth")
    instance = RealEstateMedia.objects.create(
        landlord=request.user,
        file=request.FILES['file']
    )
    return JsonResponse({
        "id": instance.pk,
        "file": instance.file.url
    })