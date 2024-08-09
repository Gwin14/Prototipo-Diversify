from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# Create your models here.


class Vaga(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    company_description = models.TextField(blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    tags = TaggableManager()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
