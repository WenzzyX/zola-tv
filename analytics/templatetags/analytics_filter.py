from django import template

register = template.Library()

def get_class_name(value):
    return value.__class__.__name__

register.filter('get_class_name', get_class_name)