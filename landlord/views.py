from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from property.models import Contract, RealEstate, RealEstateMedia, Transaction
import json

from user.mixins import LandlordContentOnlyMixin


class TransactionSingleView(LoginRequiredMixin, LandlordContentOnlyMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'landlord/transaction.html'

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
