from django import template

register = template.Library()

@register.filter
def get_dict_item(d, key):
    if isinstance(d, dict):
        return d.get(str(key), '')
    return ''
