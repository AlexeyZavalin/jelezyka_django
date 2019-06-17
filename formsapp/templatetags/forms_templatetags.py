from django import template
from formsapp.forms import RegisterForm, CallMeForm, RequestForm

register = template.Library()


@register.inclusion_tag('formsapp/register_form.html')
def register_form():
    form = RequestForm
    return {'form': form}


@register.inclusion_tag('formsapp/request_form.html')
def request_form():
    form = RequestForm
    return {'form': form}


@register.inclusion_tag('formsapp/call_me_form.html')
def call_me_form():
    form = RequestForm
    return {'form': form}