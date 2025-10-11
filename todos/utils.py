from .models import Task

def get_object(self, pk):
    """
    Obtain task and verify permissions
    """
    try:
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(self.request, task)
        return task
    except Task.DoesNotExist:
        return None