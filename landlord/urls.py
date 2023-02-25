from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard-landlord"),
    path('real-estate/overview', RealEstateOverview.as_view(), name="real-estate-overview"),
    path('real-estate/overview/<str:key>', RealEstateOverviewSingle.as_view(), name="real-estate-overview-single"),
    path('real-estate/create', RealEstateCreate.as_view(), name="real-estate-create"),
    path('real-estate/update/<str:key>', RealEstateUpdate.as_view(), name="real-estate-update"),
    path('real-estate/delete/<str:key>', RealEstateDelete.as_view(), name="real-estate-delete"),

    path('real-estate/transactions', TransactionsView.as_view(), name="real-estate-transactions"),
    path('real-estate/transaction/<str:key>', TransactionSingleView.as_view(), name="real-estate-transaction-single"),

    path('real-estate/meterpoints', MeterPointsView.as_view(), name="meterpoints-landlord"),
    path('real-estate/meterpoint/<str:key>', MeterPointSingleView.as_view(), name="single-meterpoint-landlord"),

    path('real-estate/requests', RequestsAllView.as_view(), name="requests-landlord"),
    path('real-estate/requests/add', RequestsAddView.as_view(), name="add-requests-landlord"),
    path('real-estate/requests/<str:key>', RequestsByRealEstateView.as_view(), name="requests-by-real-estate-landlord"),

    path('real-estate/contracts', RealEstateContracts.as_view(), name="contracts-landlord"),
    path('real-estate/contracts/<str:key>', RealEstateContractSingle.as_view(), name="single-contract-landlord"),

    path('real-estate/contract/approve/<int:pk>', RealEstateContractApprove.as_view(), name="approve-contract-landlord"),
    path('real-estate/contract/decline/<int:pk>', RealEstateContractDecline.as_view(), name="decline-contract-landlord"),

]