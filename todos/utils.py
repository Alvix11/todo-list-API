from .models import Task

def get_task(pk):
    
    try:
        task = Task.objects.get(pk=pk)
        return task
    except Task.DoesNotExist:
        return None
    
def get_task_user(pk, user):
    
    task = get_task(pk=pk)
    
    if task is None:
        return 404
    
    if task.user == user:
        return task
    else:
        return 403