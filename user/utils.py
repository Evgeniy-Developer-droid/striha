from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.utils import timezone
from property.models import Contract, RealEstate



def get_summary(user):

    def get_time_text(target_date, action):
        now = timezone.now()
        time_between = now.timestamp() - target_date.timestamp()
        time_between_seconds = time_between
        years = time_between_seconds / 60 / 60 / 24 / 365.25
        months = time_between_seconds / 60 / 60 / 24 / 30
        days = time_between_seconds / 60 / 60 / 24
        hours = time_between_seconds / 60 / 60

        if action == "login":
            if years >= 1:
                return f"останій вхід {int(years)} років тому"
            if months >= 1:
                return f"останій вхід {int(months)} місяців тому"
            if days >= 1:
                return f"останій вхід {int(days)} днів тому"
            if hours >= 1:
                return f"останій вхід {int(hours)} годин тому"
            return "останій вхід недавно"
        else:
            if years >= 1:
                return f"на сервісі {int(years)} роки"
            if months >= 1:
                return f"на сервісі {int(months)} місяці"
            return "на сервісі недавно"
        

    result = dict()
    result['last_login'] = get_time_text(user.last_login, 'login')
    result['joined'] = get_time_text(user.date_joined, 'register')
    if user.role == 'landlord':
        real_estates = RealEstate.objects.filter(landlord=user)
        contracts_all = Contract.objects.filter(landlord=user)
        contracts_active = contracts_all.filter(status='active')
        result['real_estates'] = real_estates.count()
    else:
        contracts_all = Contract.objects.filter(tenant=user)
        contracts_active = contracts_all.filter(status='active')
    
    result['contracts_all'] = contracts_all.count()
    result['contracts_active'] = contracts_active.count()
    return result


def get_dashboard_link(role):
    if role == "landlord":
        return reverse('dashboard-landlord')
    return reverse('dashboard-tenant')