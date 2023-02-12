from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard-tenant"),
    path('contract', ContractView.as_view(), name="contract-tenant"),
    path('contract/new', NewContractView.as_view(), name="new-contract-tenant"),
    path('contract/steps', StepsContractView.as_view(), name="steps-contract-tenant"),
]