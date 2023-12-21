from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.urls import reverse


# Модель для объявлений
class Announcement(models.Model):

    class Category(models.TextChoices):
        TANK = 'TN', 'Танки'
        HEAL = 'HL', 'Хилы'
        DD = 'DD', 'ДД'
        BUYERS = 'BR', 'Торговцы'
        GUILDMASTER = 'GM', 'Гилдмастеры'
        QUESTGIVER = 'QG', 'Квестгиверы'
        BLACKSMITH = 'BS', 'Кузнецы'
        TANNER = 'TR', 'Кожевники'
        POTIONMASTER = 'PM', 'Зельевары'
        SPELLMASTER = 'SP', 'Мастера заклинаний'

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.TANK, verbose_name='Категория')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    content_media = models.FileField(upload_to='forum/%Y/%m/%d/', blank=True, null=True, verbose_name='Медиа')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'announcement_id': self.pk})


# Модель для откликов
class Response(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, verbose_name='Объявление')
    text = models.TextField(verbose_name='Текст')
    status = models.BooleanField(default=False, verbose_name='Статус')

    def __str__(self):
        return f'Отклик на {self.announcement.title}'

    def get_absolute_url(self):
        return reverse('response', kwargs={'pk': self.pk})

