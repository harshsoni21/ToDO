from django.db import models
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
]

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        db_table = "tasks"

    def __str__(self):
        return f"{self.id} - {self.title}"