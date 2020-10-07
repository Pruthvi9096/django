from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field,cls):
    try:
        return field.as_widget(attrs={'class':cls})
    except:
        pass