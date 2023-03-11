from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard-tenant"),

    path('contract/new', NewContractView.as_view(), name="new-contract-tenant"),

    path('transactions', TransactionsView.as_view(), name="real-estate-transactions-tenant"),
    path('transaction/<str:key>', TransactionSingleView.as_view(), name="real-estate-transaction-single-tenant"),

    path('meterpoints', MeterPointsView.as_view(), name="meterpoints-tenant"),
    path('meterpoint/<str:key>', MeterPointSingleView.as_view(), name="single-meterpoint-tenant"),

    path('contracts', RealEstateContracts.as_view(), name="contracts-tenant"),
    path('contracts/<str:key>', RealEstateContractSingle.as_view(), name="single-contract-tenant"),

    path('requests', RequestsAllView.as_view(), name="requests-tenant"),
    path('requests/add', RequestsAddView.as_view(), name="add-requests-tenant"),
    path('requests/<str:key>', RequestsByRealEstateView.as_view(), name="requests-by-real-estate-tenant"),

    path('notifications', NotificationsView.as_view(), name="notifications-tenant"),
]