from django import template
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