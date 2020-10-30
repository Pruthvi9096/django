from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field,cls):
    try:
        return field.as_widget(attrs={'class':cls})
    except:
        pass

@register.filter(name='add_value')
def add_value(field,value):
    try:
        return field.as_widget(attrs={'value':value})
    except:
        pass
