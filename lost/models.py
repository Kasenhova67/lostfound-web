from django.db import models
from django.contrib.auth.models import User

class itemlost(models.Model):
    product_title = models.CharField(max_length=100)
    place = models.TextField(default='Lost this item near ..')
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    contactme = models.CharField(max_length=150, default='email')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='lost_items')
    username = models.CharField(max_length=100, blank=True, default='NULL')

    def __str__(self):
        return f'{self.username} lost {self.product_title}'

class itemfound(models.Model):
    product_title = models.CharField(max_length=100)
    place = models.TextField(default='Found this item near ..')
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    contactme = models.CharField(max_length=150, default='email')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='found_items')
    username = models.CharField(max_length=100, blank=True, default='NULL')

    def __str__(self):
        return f'{self.username} found {self.product_title}'