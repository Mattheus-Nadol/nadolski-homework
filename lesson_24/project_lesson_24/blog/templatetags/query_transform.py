from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """Return encoded querystring with `field` set to `value`, preserving other GET params."""
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()

