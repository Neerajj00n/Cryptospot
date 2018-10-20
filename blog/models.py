# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from datetime import datetime
from slugify import slugify
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Blog(models.Model):

	author = models.ForeignKey(User)
	title = models.CharField(max_length=120)
	content = RichTextUploadingField()
	box_image = models.ImageField(upload_to="Blog/",blank=True,null=True)
	published_on = models.DateTimeField(default=datetime.now,blank=True,null=True, editable=False)
	slug = models.SlugField(max_length=255, null=True, blank=True, editable=False)

	def save(self, *args, **kwargs):
	   	
	   	self.slug = slugify(self.title)
		super(Blog, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title