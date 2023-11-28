from django import template

register = template.Library()

@register.simple_tag
def calculate_order(page_number, counter, per_page=2):
    return (page_number - 1) * per_page + counter
