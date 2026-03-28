from django.db import models

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_completed=False)

# Create your models here.
class Task(models.Model):
    class Period(models.TextChoices):
        YEAR = 'year', 'Год'
        QUARTER = 'quarter', 'Квартал'
        MONTH = 'month', 'Месяц'
        WEEK = 'week', 'Неделя'
        DAY = 'day', 'День'


    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    objects = models.Manager()
    active =  ActiveManager()
    period = models.CharField(
        max_length=10,
        choices=Period.choices,
        default=Period.DAY
    )


    class Meta:
        ordering = ['id']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title