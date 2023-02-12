

from django.shortcuts import redirect


class LandlordContentOnlyMixin():
    """Check role - only for landlord else redirect"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == "tenant":
                return redirect("dashboard-tenant")
        return super().dispatch(request, *args, **kwargs)


class TenantContentOnlyMixin():
    """Check role - only for tenant else redirect"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == "landlord":
                return redirect("dashboard-landlord")
        return super().dispatch(request, *args, **kwargs)