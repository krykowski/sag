from django import template

from account.forms import UserLoginForm

register = template.Library()

@register.inclusion_tag('account/tags/login.html')
def login_form():
    form = UserLoginForm()
    
    return {'form': form}