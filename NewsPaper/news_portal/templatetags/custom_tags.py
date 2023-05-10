from django import template


register = template.Library()


# Регистрируем наш тэг под именем url_replace, чтоб Django понимал,
# что это именно тэг для шаблонов, а не простая функция.
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()