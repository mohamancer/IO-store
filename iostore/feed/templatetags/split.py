from django import template

register = template.Library()


@register.filter(name='split')
def split(value):
    a = value.split(",")
    if len(a) > 0:
        return a[0]
    else:
        return value
