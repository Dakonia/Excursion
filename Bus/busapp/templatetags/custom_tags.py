from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Возвращает диапазон от 0 до value - 1."""
    return range(value)