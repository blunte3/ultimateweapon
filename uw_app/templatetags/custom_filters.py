from django import template
from uw_app.models import Task

register = template.Library()

@register.filter(name='get_task_from_id')
def get_task_from_id(task_id):
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None