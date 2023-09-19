# custom_filters.py

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def truncate_lines(value, num_lines):
    lines = value.split('\n')
    if len(lines) <= num_lines:
        return value
    truncated_lines = lines[:num_lines]
    return '\n'.join(truncated_lines) + ' ...'