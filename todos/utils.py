from .models import Task

def get_task(pk, user):
    
    try:
        task = Task.objects.get(pk=pk, user=user)
        return task
    except Task.DoesNotExist:
        task = None
        return task