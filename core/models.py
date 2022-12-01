from django.db import models


# Create your models here.

class Newsletter(models.Model):
    topic_parser = models.URLField(
        verbose_name='Топик из которого нужно парсить'
    )
    topic_donor = models.URLField(
        verbose_name='Топик в который нужно загружать'
    )
    post_datetime = models.TimeField(
        verbose_name='Когда нужно загрузить',
    )
    days_ago = models.PositiveIntegerField(
        verbose_name='Насколько дней назад уйти для загрузки сообщений ?',
        default=1
    )

    def __str__(self):
        return str(self.post_datetime)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
