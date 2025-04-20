from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError

# Пользователь
class User(AbstractUser):
    ROLE_CHOICES = (
        ('veteran',   'Ветеран'),
        ('volunteer', 'Волонтёр'),
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Формат телефона: '+999999999'. До 15 цифр."
    )

    # Поля
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    city = models.CharField("Город проживания", max_length=100)
    phone = models.CharField(
        "Телефон", 
        max_length=20, 
        validators=[phone_regex],
        blank=False
    )

    # Кем является пользователь
    def is_veteran(self):
        return self.role == 'veteran'
    def is_volunteer(self):
        return self.role == 'volunteer'

# Запросы на помощь ветеранов
class HelpRequest(models.Model):
    HELP_TYPES = (
        ('shopping', 'Закупки'),
        ('medical',  'Медпомощь'),
        ('walk',     'Прогулка'),
        ('other',    'Другое'),
    )
    STATUS_CHOICES = (
        ('open',        'Открыта'),
        ('in_progress', 'В работе'),
        ('done',        'Выполнено'),
    )
    veteran = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    help_type   = models.CharField("Тип помощи", max_length=20, choices=HELP_TYPES)
    description = models.TextField(
        "Описание",
        validators=[MinLengthValidator(10)],
        max_length=1000
    )
    location    = models.CharField("Местоположение", max_length=200)
    status      = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='open')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_help_type_display()} в {self.location} ({self.get_status_display()})"

    def clean(self):
        if not self.veteran_id:
            return  # Пропускаем проверку если ветеран еще не установлен
            
        # Проверка количества активных заявок
        active_requests = HelpRequest.objects.filter(
            veteran=self.veteran,
            status__in=['open', 'in_progress']
        ).count()
        
        # Не считаем текущую заявку если она уже существует
        if self.pk:
            active_requests -= 1
            
        if active_requests >= 3:
            raise ValidationError('У вас уже есть 3 активные заявки')

class Application(models.Model):
    help_request = models.ForeignKey(
        HelpRequest,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    volunteer    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    contact_info = models.TextField(
        "Контактные данные",
        validators=[MinLengthValidator(10)],
        max_length=500
    )
    created_at   = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Skip validation if volunteer is not set yet
        if not hasattr(self, 'volunteer') or self.volunteer is None:
            return
            
        # Проверка количества заявок волонтера
        active_applications = Application.objects.filter(
            volunteer=self.volunteer,
            help_request__status='in_progress'
        ).count()
        if active_applications >= 2:
            raise ValidationError('Вы уже помогаете по 2 заявкам')