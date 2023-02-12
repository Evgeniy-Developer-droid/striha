from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from property.models import Contract, Transaction
from django.conf import settings
from tenant.logic import create_contract

from user.mixins import TenantContentOnlyMixin


class StepsContractView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/steps_contract.html'

    def get(self, request):
        
        contract = Contract.objects.filter(tenant=request.user).exclude(status__in=["terminated", "declined"]).order_by('-created')
        if contract.exists():
            contract = contract.first()
            if contract.status == "active":
                return redirect(reverse("contract-tenant"))
            return render(request, self.template_name, {"contract": contract})
        return redirect(reverse("new-contract-tenant"))


class NewContractView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/new_contract.html'

    def get(self, request):
        contract = Contract.objects.filter(tenant=request.user).exclude(status__in=["terminated", "declined"]).order_by('-created')
        if contract.exists():
            contract = contract.first()
            if contract.status == "active":
                return redirect(reverse("contract-tenant"))
            else:
                return redirect(reverse("steps-contract-tenant"))
        return render(request, self.template_name, {})
    
    def post(self, request):
        if request.POST.get("action", "") == "create_contract":
            res = create_contract(request)
            if res[0]:
                return redirect(reverse("steps-contract-tenant"))
            return render(request, self.template_name, {"error": res[1]})


class ContractView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/contract.html'

    def get(self, request):
        contract = Contract.objects.filter(tenant=request.user).exclude(status__in=["terminated", "declined"]).order_by('-created')
        if contract.exists():
            contract = contract.first()
            if contract.status == "active":
                return render(request, self.template_name, {})
            else:
                return redirect(reverse("steps-contract-tenant"))
        return redirect(reverse("new-contract-tenant"))


class Dashboard(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/dashboard.html'

    def get(self, request):
        transactions = Transaction.objects.filter(tenant=request.user).order_by('-created')[:10]
        contract = Contract.objects.filter(tenant=request.user).exclude(status__in=["terminated", "declined"]).order_by('-created')
        if contract.exists():
            contract = contract.first()
        return render(request, self.template_name, {
            "contract": contract,
            "transactions": transactions
        })
