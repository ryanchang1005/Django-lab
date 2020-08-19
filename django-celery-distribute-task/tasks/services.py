from tasks.models import Task


class TaskService:

    @staticmethod
    def batch_create(n):
        tasks = []

        for i in range(n):
            tasks.append(Task())

        if len(tasks) == 0:
            return None
        Task.objects.bulk_create(tasks)
