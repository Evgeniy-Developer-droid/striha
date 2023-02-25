from django.urls import path

from property.api import delete_real_estate_media, get_contract_status_tenant, \
    upload_real_estate_media, get_real_estate_by_token, request_media_upload, delete_request_media

urlpatterns = [

    # callbacks

    # api
    path('real-estate/media/upload', upload_real_estate_media, name="real-estate-media-upload"),
    path('real-estate/media/delete', delete_real_estate_media, name="real-estate-media-delete"),
    path('real-estate/get-by-token', get_real_estate_by_token, name="real-estate-get-by-token"),
    path('real-estate/contract-check-status', get_contract_status_tenant, name="contract-check-status"),

    path('real-estate/request/media/upload', request_media_upload, name="request-media-upload"),
    path('real-estate/request/media/delete', delete_request_media, name="request-media-delete"),
]