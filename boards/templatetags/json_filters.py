from django import template
import json
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()

@register.filter(is_safe=True)
def to_json(value):
    return json.dumps(value, cls=DjangoJSONEncoder)
