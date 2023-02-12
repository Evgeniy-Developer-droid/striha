

from property.models import Contract, OtherContractTenant, RealEstate


def create_contract(request):
    try:
        real_estate = RealEstate.objects.get(share_token=request.POST.get("token", "empty"))
        if real_estate.status == "rented":
            return False, "Real Estate already rented"
        if real_estate.status == "disable":
            return False, "Real Estate disabled"

        contract = Contract.objects.create(
            tenant=request.user,
            landlord=real_estate.landlord,
            price_month=real_estate.price_month,
            price_security=1,
            real_estate=real_estate,
        )

        index = 0
        for key in request.POST.keys():
            if key.startswith(f"sub_{index}"):
                OtherContractTenant.objects.create(
                    first_name=request.POST.get(f'sub_{index}_fn'),
                    last_name=request.POST.get(f'sub_{index}_ln'),
                    email=request.POST.get(f'sub_{index}_em'),
                    contract=contract
                )
                index += 1
        return True, "Success"
    except RealEstate.DoesNotExist:
        return False, "Failed"