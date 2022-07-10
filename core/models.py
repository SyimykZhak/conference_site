from atexit import register
from collections import Counter
from django.db import models
from datetime import date
from django.utils import timezone
from django.urls import reverse

from django.db.models import FloatField, Avg, Max

# Create your models here.


class Speakers(models.Model):
    name = models.CharField("Имя", max_length=20,blank=False)
    age = models.PositiveSmallIntegerField("Возраст", default=0,blank=False)
    description = models.TextField("Описание",blank=False)
    image = models.ImageField("Изображение",blank=False, upload_to="speakers/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speakers_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Спикеры"
        verbose_name_plural = "Спикеры"

class Conference(models.Model):
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    about = models.TextField("О нас",blank=False)
    description = models.TextField("Описание")
    poster = models.ImageField("Шаблон", blank=False)
    address = models.CharField("Cтрана и  город", max_length=30,blank=False)
    street = models.CharField("Улица", max_length=30,blank=False)
    place = models.CharField("Место проведение", max_length=30, blank=False)
    email = models.EmailField("Email конференции")
    telephone = models.CharField("Телефон", max_length=15,blank=False)
    map = models.URLField(verbose_name="ссылка к карту", blank=False)
    tickets = models.PositiveSmallIntegerField("Колчество билетов", default=0)
    ostatok_tickets = models.PositiveSmallIntegerField("Остаток билетов", default=0)
    kol_speakers = models.PositiveSmallIntegerField("количество спикеров", default=0)
    speakers = models.ManyToManyField(Speakers, verbose_name="спикеры", related_name="conference_speakers")
    date = models.DateField("Дата", default=date.today)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("conference_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференция"


class Program(models.Model):
    start_time = models.TimeField("Начало выступление")
    end_time = models.TimeField("Конец выступление")
    description = models.CharField("описание", max_length=20,blank=True)
    speaker = models.CharField("спикер", max_length=20,blank=True)
    conference = models.ForeignKey(Conference,on_delete=models.CASCADE,blank=True, related_name="conference_name")
    
    class Meta:
        verbose_name = "Программы"
        verbose_name_plural = "программа конференции"


class Register(models.Model):
    name = models.CharField("Имя", max_length=100)
    lastname = models.CharField("Фамилия", max_length=100)
    age = models.PositiveSmallIntegerField("возраст", default=0)
    email = models.EmailField("Email")
    telephone = models.CharField("Телефон", max_length=15)
    addres  = models.CharField("Адрес",max_length=200, blank=True, null=True)
    conference = models.ForeignKey(Conference, verbose_name="конференция", on_delete=models.CASCADE)
    created = models.DateTimeField("Дата регистрации",auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.update_at = timezone.now()
        return super(Register, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Зарегистрированные"


class Partners(models.Model):
    title = models.CharField("Описание компании", max_length=100)
    description = models.TextField("О компании")
    logo = models.ImageField("Логотип компании", blank=False)
    conference = models.ForeignKey(Conference, verbose_name="конференция", on_delete=models.CASCADE, related_name="partners")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "партнеры"

class Work(models.Model):
    title = models.CharField("Описание работы", max_length=100)
    work = models.FileField("Работа участника",blank=False, upload_to="work/")
    conference = models.ForeignKey(Conference, verbose_name="конференция", on_delete=models.CASCADE)
    created = models.DateTimeField("дата отправки",auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Работа участника"


