from django.contrib import admin
from .models import RealEstate, Contract, RealEstateMedia, OtherContractTenant, Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("name", "tenant", 
    "landlord", "amount", "status")
    ordering = ('-created',)


admin.site.register(Transaction, TransactionAdmin)



class RealEstateMediaTabular(admin.TabularInline):
    model = RealEstateMedia
    extra = 1

class RealEstateAdmin(admin.ModelAdmin):
    list_display = ("title", )
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
    list_display = ("real_estate", "tenant", 
    "landlord", "price_month", "price_security", "status")
    fieldsets = (
        ("Contract Info", {"fields": (("real_estate", "tenant", "landlord",), 
                                        ("price_month", "price_security", "status",),)}),
    )
    search_fields = ('real_estate__title',)
    ordering = ('-created',)
    inlines = [OtherContractTenantTabular]


admin.site.register(Contract, ContractAdmin)
