from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter
def remove_newlines(input_array):
    output_array = []
    for item in input_array:
        cleaned_item = item.replace("\n", "")
        output_array.append(cleaned_item)
    return output_array

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)





@register.filter
@stringfilter
def strip(value):
    # Remove HTML tags
    value = re.sub('<[^>]*>', '', value)
    # Remove whitespace
    value = ''.join(value.split())
    return value

@register.filter
@stringfilter
def strip_length(value):
    # Remove HTML tags
    value = re.sub('<[^>]*>', '', value)
    # Remove whitespace
    value = ''.join(value.split())
    return len(value)
