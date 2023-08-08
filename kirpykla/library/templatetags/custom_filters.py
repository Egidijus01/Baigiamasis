from django import template


register = template.Library()

@register.filter(name='create_range')
def create_range(value):
    return range(value)

@register.filter(name='convert_int')
def convert_int(value):
    return int(value)