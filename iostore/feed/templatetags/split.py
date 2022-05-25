from django import template

register = template.Library()


@register.filter(name='split')
def split(value,arg):
    a = value.split(",")
    if arg==2:
        return a[0]+ ', '+ a[1]
    else:
        if len(a) > 0:
            return a[0]
        else:
            return value
