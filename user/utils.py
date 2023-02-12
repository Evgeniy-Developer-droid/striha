from django.urls import reverse, reverse_lazy

def get_dashboard_link(role):
    if role == "landlord":
        return reverse('dashboard-landlord')
    return reverse('dashboard-tenant')