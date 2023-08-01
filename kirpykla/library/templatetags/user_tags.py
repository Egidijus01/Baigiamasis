from django import template
from django.contrib.auth.models import Group
from library.apps import LibraryConfig  # Import the AppConfig containing the ready method

register = template.Library()

@register.filter
def in_kirpejai_group(user):
    try:
        kirpejai_group = Group.objects.get(name='kirpejai')
        return kirpejai_group in user.groups.all()
    except Group.DoesNotExist:
        return False