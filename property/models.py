from django.db import models
from authentification.utils import generate_token
from user.models import User


class RealEstate(models.Model):
    STATUS = (
        ('not_rented', "Not rented",),
        ('disable', "Disable",),
        ('rented', "Rented",),
    )
    TYPE_REAL_ESTATE = (
        ('house', 'House',),
        ('appartment', 'Appartment',),
        ('single_room', 'Single room',),
    )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default="New Real Estate", blank=True)
    description = models.TextField(default="", blank=True)
    status = models.CharField(max_length=255, choices=STATUS, default="not_rented", blank=True)
    type_real_estate = models.CharField(max_length=255, choices=TYPE_REAL_ESTATE, default="house", blank=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="real_estate_landlord", null=True)

    smokers_allowed = models.BooleanField(default=False)
    children_allowed = models.BooleanField(default=False)
    students_allowed = models.BooleanField(default=False)
    animals_allowed = models.BooleanField(default=False)

    rooms = models.IntegerField(blank=True, default=1)
    floor = models.IntegerField(blank=True, default=1)
    tenants = models.IntegerField(blank=True, default=1)

    price_month = models.IntegerField(default=0)
    share_token = models.CharField(max_length=255, blank=True, default=generate_token)

    def __str__(self):
        return f"{self.title}:pk--{self.pk}"


class RealEstateMedia(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to='realestate', null=True, blank=True)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True, related_name="real_estate_media")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="real_estate_media_landlord", null=True)


class Contract(models.Model):
    STATUS = (
        ("active", "Active"), # last

        ("declined", "Declined"), 
        ("pending_landlord", "Pending Landlord"), # first

        ("terminated", "Terminated"),
    )
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS, default="pending_landlord")
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contract_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contract_landlord")
    price_month = models.IntegerField(default=0)
    price_security = models.IntegerField(default=0)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name="contract_real_estate")


class OtherContractTenant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255, default="", blank=True)
    last_name = models.CharField(max_length=255, default="", blank=True)
    email = models.EmailField(max_length=255, default="", blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="other_contract_tenant")


class MeterPoint(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meter_point_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meter_point_landlord")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="meter_point_contract")
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True, related_name="meter_point_real_estate")
    period = models.CharField(max_length=255, default="")  # December, 2022
    image = models.ImageField(upload_to="meterpoints")
    name = models.CharField(max_length=255, default="")
    value = models.CharField(max_length=255, default="")
    Other = models.TextField(default="", blank=True)


class Invoice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoice_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoice_landlord")


class Transaction(models.Model):
    STATUS = (
        ('failed', 'Failed',),
        ('success', 'Success',),
        ('pending', 'Pending',),
    )
    created = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_landlord")
    amount = models.IntegerField(default=0)
    sender_commission = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=STATUS, default="pending")
    order_id = models.CharField(default="", max_length=255)
    liqpay_order_id = models.CharField(default="", max_length=255)
    name = models.CharField(max_length=255, default="default")
    sender_card_type = models.CharField(max_length=255, default="", blank=True)
    payment_id = models.CharField(max_length=255, default="", blank=True)
    transaction_id = models.CharField(max_length=255, default="", blank=True)
    card_mask = models.CharField(max_length=255, default="", blank=True)
    meta = models.TextField(default="{}", blank=True)

