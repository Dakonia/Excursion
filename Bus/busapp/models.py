from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError


# Для суперпользователя
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('username', email.split('@')[0])

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password=password, **extra_fields)

# Роли пользователя
class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('company', 'Транспортная компания'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=150, blank=True, null=True)  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  
    objects = UserManager() 

    def is_client(self):
        return self.role == 'client'

    def is_company(self):
        return self.role == 'company'



# Клиент
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    STATUS = (
        ('legal_entity', 'Юридическое лицо'),
        ('individual', 'Физическое лицо'),
    )
    MALE = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )
    email = models.EmailField(unique=True, verbose_name='Почта')
    status = models.CharField(max_length=20, choices= STATUS, verbose_name='Cтатус')
    name = models.CharField(max_length=20, verbose_name= 'Имя клиента или организации')
    surname = models.CharField(max_length=15, null=True, blank=True, verbose_name='Фамилия')
    surname2 = models.CharField(max_length=15, null=True, blank=True, verbose_name='Отчество')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    male = models.CharField(max_length=20, choices=MALE, null=True, blank=True, verbose_name='Пол')
    number = models.CharField(max_length=10, null=True, blank=True, verbose_name='Телефоный номер')
    image = models.ImageField(upload_to='avatar_client/', null=True, blank= True, default= None, verbose_name='Аватарка')

    def __str__(self):
        return self.name


# ТК
class TransportCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255, help_text="Название транспортной компании")
    email = models.EmailField(unique=True, verbose_name='Почта')
    STATUS = (
        ('legal_entity', 'Юридическое лицо'),
        ('individual', 'Физическое лицо'),
    )
    status = models.CharField(max_length=20, choices= STATUS, verbose_name='Cтатус')
    image = models.ImageField(upload_to='avatar_company/', null=True, blank= True, default= None, verbose_name='Аватарка')
    TIN = models.CharField(max_length=20, null=True, blank=True, verbose_name='ИНН компании')
    description = models.TextField(null=True, blank=True, verbose_name='Описние компнаии')

    def __str__(self):
        return self.company_name
    
    def get_average_rating(self):
        reviews = self.reviews.all() 
        if reviews.exists():
            total_stars = sum(review.stars for review in reviews)
            return total_stars / reviews.count()
        return 0

# Особености
class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Название особенности (например: Wi-Fi, кондиционер)")
    images = models.ImageField(upload_to='feature/', null=True, blank=True, verbose_name='Фото доп утсановок')


    def __str__(self):
        return self.name
    
    
# Функционал
class Functionality(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Дополнительный функционал')

    def __str__(self):
        return self.name
    

# Системы безопасности
class Safety(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Системы безопасности')

    def __str__(self):
        return self.name


# Автобус
class Bus(models.Model):
    MODEL = (
        ('minibus', 'Микроавтобус'),
        ('minivan', 'Минивен'),
        ('bus', 'Автобус'),
        ('double_bus', 'Двухэтажные'),
        ('long_bus', 'Дальнего следования'),
    )
    transport_company = models.ForeignKey('TransportCompany', on_delete=models.CASCADE, related_name='buses')
    # created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, help_text="Название автобуса", verbose_name='Название автобуса')
    seats = models.PositiveIntegerField(help_text="Количество мест", verbose_name='Количество мест')
    type = models.CharField(max_length=15, choices=MODEL, verbose_name='Типо автобуса')
    features = models.ManyToManyField(Feature, blank=True, related_name='buses', help_text="Особенности автобуса", verbose_name='Доп функции автобуса')
    functionality = models.ManyToManyField(Functionality, related_name='buses', blank=True, verbose_name='Дополнительный функционал')
    safety = models.ManyToManyField(Safety, related_name='buses', blank=True, verbose_name='Системы безопасности')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Стоимость аренды за день", verbose_name='Стоимость аренды')
    available = models.BooleanField(default=True, help_text="Доступен ли автобус для аренды", verbose_name='Доступность автобуса')
    description = models.TextField(null=True, blank=True, verbose_name='Описание автобуса')
    image = models.ImageField(upload_to='buses/', null=True, blank=True, verbose_name='фото автобуса')
    long_trips = models.BooleanField(default=False, verbose_name='Долгие поездки и аренда')

    def __str__(self):
        return self.name
    
    def is_available_on_date(self, date):
        return not self.orders.filter(date=date, status='confirmed').exists()



# Заказ
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('rejected', 'Отклонен'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='orders', verbose_name='Автобус')
    date = models.DateField(verbose_name='Дата поездки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    description = models.TextField(null=True, blank=True, verbose_name='Описание заказа')
    full_pirce = models.TextField(null=True, blank=True, verbose_name='Финальная цена')
    accept_client = models.BooleanField(default=None, null=True, blank=True, verbose_name='Ответ клиента')
    end_order =models.BooleanField(default=None, null=True, blank=True, verbose_name='Завершение заказа')

    def __str__(self):
        return f"Заказ от {self.client} на {self.bus.name} ({self.date})"
    
    def clean(self):
        if self.status == 'confirmed' and not self.bus.is_available_on_date(self.date):
            raise ValidationError(f"Автобус {self.bus.name} уже занят на {self.date}.")
        
# Отзыв
class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews', verbose_name='Клиент')
    transport_company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE, related_name='reviews', verbose_name='Транспортная компания')
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Оценка (звезды)')
    text = models.TextField(verbose_name='Отзыв клиента')
    response = models.TextField(null=True, blank=True, verbose_name='Ответ компании')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews', verbose_name='Заказ')

    def __str__(self):
        return f"{self.client} -> {self.transport_company}: {self.stars} stars"        
