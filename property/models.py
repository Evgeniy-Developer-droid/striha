from django.db import models
from authentification.utils import generate_token
from user.models import User
import uuid


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
    key = models.UUIDField(default=uuid.uuid4, editable=False)
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
    key = models.UUIDField(default=uuid.uuid4, editable=False)
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
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=255, choices=STATUS, default="pending_landlord")
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contract_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contract_landlord")
    price_month = models.IntegerField(default=0)
    price_security = models.IntegerField(default=0)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name="contract_real_estate")


class OtherContractTenant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, default="", blank=True)
    last_name = models.CharField(max_length=255, default="", blank=True)
    email = models.EmailField(max_length=255, default="", blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="other_contract_tenant")


class MeterPoint(models.Model):
    PERIOD_MONTH = (
        ("january", "January",),
        ("february", "February",),
        ("march", "March",),
        ("april", "April",),
        ("may", "May",),
        ("june", "June",),
        ("july", "July",),
        ("august", "August",),
        ("september", "September",),
        ("october", "October",),
        ("november", "November",),
        ("december", "December",),
    )
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meter_point_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meter_point_landlord")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meter_point_creator")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="meter_point_contract")
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True, related_name="meter_point_real_estate")
    period_title = models.CharField(max_length=255, default="")  # december 2022
    period_month = models.CharField(max_length=255, choices=PERIOD_MONTH, default="")  # december
    period_year = models.CharField(max_length=255, default="")  # 2022
    image = models.ImageField(upload_to="meterpoints")
    name = models.CharField(max_length=255, default="")
    value = models.CharField(max_length=255, default="")
    other = models.TextField(default="", blank=True)


class Transaction(models.Model):
    STATUS = (
        ('failed', 'Failed',),
        ('success', 'Success',),
        ('pending', 'Pending',),
    )
    MODE = (
        ('rent', 'Rent',),
        ('internet', 'Internet',),
        ('gas', 'Gas',),
        ('water', 'Water',),
        ('electricity', 'Electricity',),
        ('other', 'Other',),
    )
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_landlord")

    amount = models.IntegerField(default=0)

    sender_commission = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=STATUS, default="pending")
    order_id = models.CharField(default="", max_length=255, blank="")
    liqpay_order_id = models.CharField(default="", max_length=255, blank="")

    sender_card_type = models.CharField(max_length=255, default="", blank=True)
    payment_id = models.CharField(max_length=255, default="", blank=True)
    transaction_id = models.CharField(max_length=255, default="", blank=True)
    card_mask = models.CharField(max_length=255, default="", blank=True)
    meta = models.TextField(default="{}", blank=True)

    mode = models.CharField(max_length=255, choices=MODE, default="other")
    description = models.TextField(default="", blank="")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name="transaction_contract")


class Request(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name="request_contract")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_creator")
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_destination")
    viewed = models.BooleanField(default=False)

    description = models.TextField(default="", blank="")
    name = models.CharField(max_length=255, blank=True, default="")


class RequestMedia(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_media")
    file = models.ImageField(upload_to='request_media', null=True, blank=True)


class Notion(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name="notion_contract")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notion_creator")

    description = models.TextField(default="", blank="")
    name = models.CharField(max_length=255, blank=True, default="")


class NotionMedia(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    notion = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="notion_media")
    file = models.ImageField(upload_to='notion_media', null=True, blank=True)