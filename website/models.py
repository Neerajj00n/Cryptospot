# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
# Create your models here.
class Configration(models.Model):
	website_name = models.CharField(max_length=255, null=True, blank=True)
	website_headline = models.CharField(max_length=255, null=True, blank=True)
	banner = models.ImageField(upload_to="Banners/", null=True , blank=True, name="banner")
	background_banner = models.ImageField(upload_to="Banners/", null=True , blank=True, name="background_banner")

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Propic = models.ImageField(upload_to="Banners/", null=True, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

			