from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard-landlord"),
    path('real-estate/overview', RealEstateOverview.as_view(), name="real-estate-overview"),
    path('real-estate/overview/<str:key>', RealEstateOverviewSingle.as_view(), name="real-estate-overview-single"),
    path('real-estate/create', RealEstateCreate.as_view(), name="real-estate-create"),
    path('real-estate/update/<str:key>', RealEstateUpdate.as_view(), name="real-estate-update"),
    path('real-estate/delete/<str:key>', RealEstateDelete.as_view(), name="real-estate-delete"),

    path('transactions', TransactionsView.as_view(), name="real-estate-transactions"),
    path('transaction/<str:key>', TransactionSingleView.as_view(), name="real-estate-transaction-single"),

    path('settings', SettingsView.as_view(), name="settings-landlord"),

    path('meterpoints', MeterPointsView.as_view(), name="meterpoints-landlord"),
    path('meterpoint/<str:key>', MeterPointSingleView.as_view(), name="single-meterpoint-landlord"),

    path('requests', RequestsAllView.as_view(), name="requests-landlord"),
    path('requests/add', RequestsAddView.as_view(), name="add-requests-landlord"),
    path('requests/<str:key>', RequestsByRealEstateView.as_view(), name="requests-by-real-estate-landlord"),

    path('contracts', RealEstateContracts.as_view(), name="contracts-landlord"),
    path('contracts/<str:key>', RealEstateContractSingle.as_view(), name="single-contract-landlord"),

    path('contract/approve/<int:pk>', RealEstateContractApprove.as_view(), name="approve-contract-landlord"),
    path('contract/decline/<int:pk>', RealEstateContractDecline.as_view(), name="decline-contract-landlord"),

]

