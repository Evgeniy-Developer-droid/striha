from django.contrib import admin
from .models import RealEstate, MeterPoint, Contract, RealEstateMedia, OtherContractTenant, Transaction, Request, RequestMedia


class RequestMediaTabular(admin.TabularInline):
    model = RequestMedia
    extra = 1

class RequestAdmin(admin.ModelAdmin):
    list_display = ("key", "name",)
    ordering = ('-created',)
    inlines = [RequestMediaTabular]


admin.site.register(Request, RequestAdmin)


class MeterPointAdmin(admin.ModelAdmin):
    list_display = ("key", "period_title",)
    ordering = ('-created',)


admin.site.register(MeterPoint, MeterPointAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("key", "tenant", 
    "landlord", "amount", "mode", "status")
    ordering = ('-created',)


admin.site.register(Transaction, TransactionAdmin)



class RealEstateMediaTabular(admin.TabularInline):
    model = RealEstateMedia
    extra = 1

class RealEstateAdmin(admin.ModelAdmin):
    list_display = ("key", "title", )
    fieldsets = (
        ("Real Estate Info", {"fields": (("title", "description",),)}),
        ("Other", {"fields": (
            ("status", "type_real_estate", "landlord", "price_month"),
            ("smokers_allowed", "children_allowed", "students_allowed", "animals_allowed",),
            ("rooms", "floor", "tenants", "share_token",),
            )}),
    )
    search_fields = ('title',)
    ordering = ('-created',)
    inlines = [RealEstateMediaTabular]


admin.site.register(RealEstate, RealEstateAdmin)


class OtherContractTenantTabular(admin.TabularInline):
    model = OtherContractTenant
    extra = 1

class ContractAdmin(admin.ModelAdmin):
    list_display = ("key", "real_estate", "tenant", 
    "landlord", "price_month", "price_security", "status")
    fieldsets = (
        ("Contract Info", {"fields": (("real_estate", "tenant", "landlord",), 
                                        ("price_month", "price_security", "status",),)}),
    )
    search_fields = ('real_estate__title',)
    ordering = ('-created',)
    inlines = [OtherContractTenantTabular]


admin.site.register(Contract, ContractAdmin)
