import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from landlord.utils import get_ua_month_value
from property.models import Contract, MeterPoint, RealEstate, RealEstateMedia, Transaction, Request, RequestMedia
import json

from user.models import Notification, User
from django.contrib.auth import update_session_auth_hash, authenticate
from .forms import NewTransactionForm

from user.mixins import LandlordContentOnlyMixin


class NotificationsView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/notifications.html'

    def get(self, request):
        new_notify = True
        not_viewed_ids = []
        print(request.GET.get('all'))
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
        return redirect(reverse("notifications-landlord"))


class SettingsView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/settings.html'

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
            return redirect(reverse("settings-landlord")+"?success=Інформація оновлена")
        if data.get('action') == "password":

            #validation
            user_check = authenticate(request, username=request.user.username, password=request.POST['old-pass'])
            if user_check is None:
                return redirect(reverse("settings-landlord")+"?error=Не правильний пароль")
            if data.get("new-pass") != data.get("rep-pass"):
                return redirect(reverse("settings-landlord")+"?error=Паролі не співпадають")

            user.set_password(data.get("new-pass"))
            user.save()
            update_session_auth_hash(request, user)
            return redirect(reverse("settings-landlord")+"?success=Пароль успішно змінено")
        return redirect(reverse("settings-landlord")+"?error=Виникла помилка")


class RequestsAddView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/requests_add.html'

    def get(self, request):
        contracts = Contract.objects.filter(landlord=request.user, status="active").order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": contracts,
        })

    def post(self, request):
        try:
            contract = Contract.objects.get(key=request.POST.get('contract', "null"), landlord=request.user)
            uploads_ids = json.loads(request.POST.get('uploads', '[]'))
            instance = Request.objects.create(
                contract=contract,
                creator=request.user,
                destination=contract.tenant,
                description=request.POST.get("description", ""),
                name=request.POST.get("name", "")
            )
            
            if uploads_ids:
                RequestMedia.objects.filter(
                    pk__in=uploads_ids).update(request=instance)
            return redirect(reverse("requests-landlord")+"?success=Запит створено.")
        except Contract.DoesNotExist:
            return redirect(reverse("requests-landlord")+"?error=Контракт не знайдено")


class RequestsByRealEstateView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/requests.html'

    def get(self, request, key):
        target = RealEstate.objects.filter(landlord=request.user, key=key)
        if target.exists():
            target = target.first()
            real_estates = RealEstate.objects.filter(landlord=request.user).exclude(key=key).order_by('-created')
            real_estates = list(real_estates)
            real_estates.insert(0,target)
            contracts = Contract.objects.filter(landlord=request.user, real_estate=target).order_by('-created')
            requests = Request.objects.filter(contract__in=[item.pk for item in contracts]).order_by('-created')
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "real_estates": real_estates,
                "requests": requests,
                "target": target
            })
        
        return redirect(reverse("requests-landlord"))


class RequestsAllView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/requests.html'

    def get(self, request):
        real_estates = RealEstate.objects.filter(landlord=request.user).order_by('-created')
        contracts = Contract.objects.filter(landlord=request.user).order_by('-created')
        requests = Request.objects.filter(contract__in=[item.pk for item in contracts]).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "real_estates": real_estates,
            "requests": requests
        })


class MeterPointSingleView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/meterpoint.html'

    def get(self, request, key):
        try:
            groups_meters = dict()
            contract = Contract.objects.get(key=key, landlord=request.user)
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
            contract = Contract.objects.get(key=key, landlord=request.user)
            # new meter point
            today = datetime.date.today()
            year = str(today.year)
            MeterPoint.objects.create(
                tenant=contract.tenant,
                landlord=request.user,
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

            return redirect(reverse("single-meterpoint-landlord", args=(key,))+"?success=")
        except Contract.DoesNotExist:
            return redirect(reverse("meterpoints-landlord")+"?error=")


class MeterPointsView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/meterpoints.html'

    def get(self, request):
        queryset = Contract.objects.filter(landlord=request.user).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": queryset,
        })


class TransactionSingleView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/transaction.html'

    def get(self, request, key):
        try:
            contract = Contract.objects.get(key=key, landlord=request.user)
            queryset = Transaction.objects.filter(contract=contract).order_by('-created')
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "transactions": queryset
            })
        except Contract.DoesNotExist:
            return render(request, self.template_name, {
                "title": "Overview Real Estate"
            })
    
    def post(self, request, key):
        try:
            contract = Contract.objects.get(key=key, landlord=request.user)

            # new transaction
            amount = request.POST.get('amount')
            mode = request.POST.get('mode', 'other')
            description = request.POST.get('description')
            Transaction.objects.create(amount=amount, 
                                        tenant=contract.tenant,
                                        contract=contract,
                                        landlord=request.user,
                                        description=description, 
                                        mode=mode)

            return redirect(reverse("real-estate-transaction-single", args=(key,))+"?success=")
        except Contract.DoesNotExist:
            return redirect(reverse("real-estate-transactions")+"?error=")


class TransactionsView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/transactions.html'

    def get(self, request):
        queryset = Contract.objects.filter(landlord=request.user).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": queryset,
        })


class RealEstateContractDecline(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_contracts.html'

    def get(self, request, pk):
        try:
            instance = Contract.objects.get(landlord=request.user, pk=pk)
            if instance.status == "pending_landlord":
                instance.status = "declined"
                instance.save()
                # send email tenant
            return redirect(reverse("contracts-landlord")+"?success=Contract declined.")
        except Contract.DoesNotExist:
            return redirect(reverse("contracts-landlord")+"?error=No access.")


class RealEstateContractApprove(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_contracts.html'

    def get(self, request, pk):
        try:
            instance = Contract.objects.get(landlord=request.user, pk=pk)
            if instance.status == "pending_landlord":
                instance.status = "active"
                instance.save()
                # send email tenant
            return redirect(reverse("contracts-landlord")+"?success=Success! Contract approved.")
        except Contract.DoesNotExist:
            return redirect(reverse("contracts-landlord")+"?error=No access.")


class RealEstateDelete(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_overview_single.html'

    def get(self, request, key):
        try:
            instance = RealEstate.objects.get(landlord=request.user, key=key)
            if instance.status != "not_rented":
                return redirect(reverse("real-estate-overview")+"?error=You can't delete. You have open contract! Please terminate contract!")
            instance.delete()
            return redirect(reverse("real-estate-overview")+"?success=Success! Deleted.")
        except RealEstate.DoesNotExist:
            return redirect(reverse("real-estate-overview")+"?error=No access.")


class RealEstateUpdate(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_update.html'

    def get(self, request, key):
        try:
            instance = RealEstate.objects.get(landlord=request.user, key=key)
            if instance.status != "not_rented":
                return render(request, self.template_name, {"error": "You can`t update. You have open contract"})
            return render(request, self.template_name, {"data": instance})
        except RealEstate.DoesNotExist:
            return render(request, self.template_name, {"error": "Not access"})

    def post(self, request, pk):
        data = request.POST
        try:
            uploads_ids = json.loads(data.get('uploads', '[]'))
            instance = RealEstate.objects.get(landlord=request.user, pk=pk)
            
            if instance.status != "not_rented":
                return render(request, self.template_name, {"error": "You can`t update. You have open contract"})

            instance.title=data.get('title')
            instance.description=data.get('description')
            instance.type_real_estate=data.get('type_real_estate')

            instance.smokers_allowed=True if "smokers_allowed" in data else False
            instance.children_allowed=True if "children_allowed" in data else False
            instance.students_allowed=True if "students_allowed" in data else False
            instance.animals_allowed=True if "animals_allowed" in data else False

            instance.rooms=int(data.get('rooms'))
            instance.floor=int(data.get('floor'))
            instance.tenants=int(data.get('tenants'))
            instance.price_month=int(data.get('price_month'))
            instance.save()

            if uploads_ids:
                RealEstateMedia.objects.filter(
                    landlord=request.user, 
                    pk__in=uploads_ids).update(real_estate=instance)
            return redirect(reverse("real-estate-overview")+"?success=Real Estate updated")
        except RealEstate.DoesNotExist:
            return redirect(reverse("real-estate-overview")+"?error=No access")


class RealEstateContractSingle(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_contract_single.html'

    def get(self, request, key):
        try:
            queryset = Contract.objects.get(key=key, landlord=request.user)
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "data": queryset,
            })
        except Contract.DoesNotExist:
            return render(request, self.template_name, {
                "title": "Overview Real Estate"
            })


class RealEstateContracts(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_contracts.html'

    def get(self, request):
        queryset = Contract.objects.filter(landlord=request.user).order_by('-created')
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "contracts": queryset,
        })


class RealEstateCreate(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_create.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        data = request.POST
        uploads_ids = json.loads(data.get('uploads', '[]'))
        instance = RealEstate.objects.create(
            landlord=request.user,
            title=data.get('title'),
            description=data.get('description'),
            type_real_estate=data.get('type_real_estate'),

            smokers_allowed=True if "smokers_allowed" in data else False,
            children_allowed=True if "children_allowed" in data else False,
            students_allowed=True if "students_allowed" in data else False,
            animals_allowed=True if "animals_allowed" in data else False,

            rooms=int(data.get('rooms')),
            floor=int(data.get('floor')),
            tenants=int(data.get('tenants')),
            price_month=int(data.get('price_month'))
        )
        if uploads_ids:
            RealEstateMedia.objects.filter(
                landlord=request.user, 
                pk__in=uploads_ids).update(real_estate=instance)
        return redirect(reverse("real-estate-overview")+"?success=Success! Created.")
        # return render(request, self.template_name, {})


class RealEstateOverviewSingle(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_overview_single.html'

    def get(self, request, key):
        try:
            queryset = RealEstate.objects.get(landlord=request.user, key=key)
            contract = Contract.objects.filter(landlord=request.user, real_estate=queryset).order_by('-created')
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "data": queryset,
                "contract": contract.first() if contract.exists() else None
            })
        except RealEstate.DoesNotExist:
            return render(request, self.template_name, {
                "title": "Overview Real Estate"
            })

class RealEstateOverview(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/RE_overview.html'

    def get(self, request):
        queryset = RealEstate.objects.filter(landlord=request.user)
        return render(request, self.template_name, {
            "title": "Overview Real Estate",
            "real_estates": queryset
        })


class Dashboard(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/dashboard.html'

    def get(self, request):
        transactions = Transaction.objects.filter(landlord=request.user).order_by('-created')[:10]
        real_estate = RealEstate.objects.filter(landlord=request.user)
        contracts = Contract.objects.filter(landlord=request.user, status="active")
        return render(request, self.template_name, {
            "real_estate": real_estate,
            "real_estate_count": real_estate.count(),
            "real_estate_not_rented": real_estate.filter(status="not_rented").count(),
            "real_estate_rented": real_estate.filter(status="rented").count(),
            "contracts": contracts.count(),
            "transactions": transactions
        })
