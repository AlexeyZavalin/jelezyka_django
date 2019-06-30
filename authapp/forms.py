from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
        'username', 'email', 'full_name', 'password1', 'password2', 'phone', 'city', 'legal', 'address_delivery')
