from django import template

register = template.Library()

@register.filter(name='integer')
def integer( value ):
    try:
        if value.is_integer(): return int(value)
        else: return value 
    except: pass
    return ''