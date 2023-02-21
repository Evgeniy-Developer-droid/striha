from django.forms import ModelForm
from property.models import Transaction



class NewTransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'mode', 'description']