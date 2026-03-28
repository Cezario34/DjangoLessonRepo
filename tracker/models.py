from django.db import models

# Create your models here.
class Habit(models.Model):
    PERIOD_CHOICES = [
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ]

    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание', blank=True)
    target_count = models.PositiveIntegerField('Цель', default=5)
    target_period = models.CharField(
        'Период цели',
        max_length = 10,
        choices = PERIOD_CHOICES,
        default = 'week'
        )
    is_active = models.BooleanField('Активна',default=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return self.title

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE,
                              related_name='logs')
    date = models.DateField('Дата')
    is_completed = models.BooleanField('Выполнено',default=False)
    created_at = models.DateTimeField(
        'Создана', auto_now_add=True
        )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Отметка привычки'
        verbose_name_plural = 'Отметка привычки'
        constraints = [
            models.UniqueConstraint(
                fields = ['habit', 'date'],
                name = 'unique_habit'
                )
        ]

        def __str__(self):
            status = '✓' if self.is_completed else '✗'
            return f'{self.habit.title} — {self.date} — {status}'