import datetime
import json
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from landlord.utils import get_ua_month_value
from property.models import Contract, MeterPoint, RealEstate, Request, RequestMedia, Transaction
from django.conf import settings
from tenant.logic import create_contract
from django.contrib.auth import update_session_auth_hash, authenticate

from user.mixins import TenantContentOnlyMixin
from user.models import Notification, User


class SettingsView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/settings.html'

    def get(self, request):
        return render(request, self.template_name, {
            "title": "Overview Real Estate"
        })

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        data = request.POST
        if data.get('action') == "summary":
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.phone = data.get("phone", user.phone)

            user.save()
            return redirect(reverse("settings-tenant")+"?success=Інформація оновлена")
        if data.get('action') == "password":

            #validation
            user_check = authenticate(request, username=request.user.username, password=request.POST['old-pass'])
            if user_check is None:
                return redirect(reverse("settings-tenant")+"?error=Не правильний пароль")
            if data.get("new-pass") != data.get("rep-pass"):
                return redirect(reverse("settings-tenant")+"?error=Паролі не співпадають")

            user.set_password(data.get("new-pass"))
            user.save()
            update_session_auth_hash(request, user)
            return redirect(reverse("settings-tenant")+"?success=Пароль успішно змінено")
        return redirect(reverse("settings-tenant")+"?error=Виникла помилка")


class RequestsAddView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/requests_add.html'

    def get(self, request):
        contracts = Contract.objects.filter(tenant=request.user, status="active").order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": contracts,
        })

    def post(self, request):
        try:
            contract = Contract.objects.get(key=request.POST.get('contract', "null"), tenant=request.user)
            uploads_ids = json.loads(request.POST.get('uploads', '[]'))
            instance = Request.objects.create(
                contract=contract,
                creator=request.user,
                destination=contract.landlord,
                description=request.POST.get("description", ""),
                name=request.POST.get("name", "")
            )
            
            if uploads_ids:
                RequestMedia.objects.filter(
                    pk__in=uploads_ids).update(request=instance)
            return redirect(reverse("requests-tenant")+"?success=Запит створено.")
        except Contract.DoesNotExist:
            return redirect(reverse("requests-tenant")+"?error=Контракт не знайдено")


class RequestsByRealEstateView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/requests.html'

    def get(self, request, key):
        contracts = Contract.objects.filter(tenant=request.user).order_by('-created')
        contract_keys = [str(item.real_estate.key) for item in contracts]
        if key not in contract_keys:
            return redirect(reverse("requests-tenant"))
        target = RealEstate.objects.filter(key=key)
        if target.exists():
            target = target.first()
            real_estates = RealEstate.objects.filter(key__in=contract_keys).exclude(key=key).order_by('-created')
            real_estates = list(real_estates)
            real_estates.insert(0,target)
            contracts = Contract.objects.filter(tenant=request.user, real_estate=target).order_by('-created')
            requests = Request.objects.filter(contract__in=[item.pk for item in contracts]).order_by('-created')
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "real_estates": real_estates,
                "requests": requests,
                "target": target
            })
        
        return redirect(reverse("requests-tenant"))


class RequestsAllView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/requests.html'

    def get(self, request):
        contracts = Contract.objects.filter(tenant=request.user).order_by('-created')
        real_estates = RealEstate.objects.filter(pk__in=list(set([item.real_estate.pk for item in contracts]))).order_by('-created')
        requests = Request.objects.filter(contract__in=[item.pk for item in contracts]).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "real_estates": real_estates,
            "requests": requests
        })


class MeterPointSingleView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/meterpoint.html'

    def get(self, request, key):
        try:
            groups_meters = dict()
            contract = Contract.objects.get(key=key, tenant=request.user)
            queryset = MeterPoint.objects.filter(contract=contract).order_by('-created')

            for item in queryset:
                if item.period_month+item.period_year not in groups_meters:
                    if len(groups_meters) >= 3:
                        break
                    groups_meters[item.period_month+item.period_year] = dict()
                    groups_meters[item.period_month+item.period_year]['data'] = list()
                    groups_meters[item.period_month+item.period_year]['title'] = item.period_title
                groups_meters[item.period_month+item.period_year]['data'].append(item)
            groups_meters = groups_meters.values()

            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "groups_meters": groups_meters
            })
        except Contract.DoesNotExist:
            return render(request, self.template_name, {
                "title": "Overview Real Estate"
            })
        
    def post(self, request, key):
        try:
            contract = Contract.objects.get(key=key, tenant=request.user)
            # new meter point
            today = datetime.date.today()
            year = str(today.year)
            MeterPoint.objects.create(
                tenant=request.user,
                landlord=contract.landlord,
                creator=request.user,
                contract=contract,
                real_estate=contract.real_estate,
                period_title=f"{get_ua_month_value(request.POST.get('period_month', 'N'))} {year}",
                period_month=request.POST.get('period_month', "N"),
                period_year=year,
                image=request.FILES['image'],
                name=request.POST.get('name', ""),
                value=request.POST.get('value', ""),
                other=request.POST.get('other', "")
            )

            return redirect(reverse("single-meterpoint-tenant", args=(key,))+"?success=")
        except Contract.DoesNotExist:
            return redirect(reverse("meterpoints-tenant")+"?error=")


class MeterPointsView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/meterpoints.html'

    def get(self, request):
        queryset = Contract.objects.filter(tenant=request.user).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": queryset,
        })


class RealEstateContractSingle(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/contract.html'

    def get(self, request, key):
        try:
            queryset = Contract.objects.get(key=key, tenant=request.user)
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "contract": queryset,
            })
        except Contract.DoesNotExist:
            return redirect(reverse("contracts-tenant"))


class RealEstateContracts(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/RE_contracts.html'

    def get(self, request):
        queryset = Contract.objects.filter(tenant=request.user).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": queryset,
        })


class NotificationsView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/notifications.html'

    def get(self, request):
        new_notify = True
        not_viewed_ids = []
        if int(request.GET.get('all', 0)) == 1:
            instances = Notification.objects.filter(target=request.user).order_by('-created')
            new_notify = False
        else:
            instances = Notification.objects.filter(target=request.user, viewed=False).order_by('-created')
            not_viewed_ids = [str(item.key) for item in instances]
        not_viewed_ids = json.dumps(not_viewed_ids)
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "data": instances,
            "new_notify": new_notify,
            "not_viewed_ids": not_viewed_ids
        })
    
    def post(self, request):
        ids = json.loads(request.POST.get("n", "[]"))
        instances = Notification.objects.filter(target=request.user, key__in=ids)
        instances.update(viewed=True)
        return redirect(reverse("notifications-tenant"))


class TransactionsView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/transactions.html'

    def get(self, request):
        queryset = Contract.objects.filter(tenant=request.user).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": queryset,
        })


class TransactionSingleView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/transaction.html'

    def get(self, request, key):
        try:
            contract = Contract.objects.get(key=key, tenant=request.user)
            queryset = Transaction.objects.filter(contract=contract).order_by('-created')
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "transactions": queryset
            })
        except Contract.DoesNotExist:
            return render(request, self.template_name, {
                "title": "Overview Real Estate"
            })


class NewContractView(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/new_contract.html'

    def get(self, request):
        return render(request, self.template_name, {})
    
    def post(self, request):
        if request.POST.get("action", "") == "create_contract":
            res = create_contract(request)
            if res[0]:
                return redirect(reverse("steps-contract-tenant"))
            return render(request, self.template_name, {"error": res[1]})


class Dashboard(LoginRequiredMixin, TenantContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'tenant/dashboard.html'

    def get(self, request):
        transactions = Transaction.objects.filter(tenant=request.user).order_by('-created')[:10]
        contract = Contract.objects.filter(tenant=request.user)
        return render(request, self.template_name, {
            "contract": contract,
            "transactions": transactions
        })
