from django.forms import ModelForm
from formsapp.models import Register, Request, CallMe


class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = ['email', 'phone', 'comment']


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['vin', 'number_or_name', 'name', 'phone', 'email']


class CallMeForm(ModelForm):
    class Meta:
        model = CallMe
        fields = ['email', 'phone']
