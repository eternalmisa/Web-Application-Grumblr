# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0022_auto_20151005_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='block',
            field=models.ManyToManyField(related_name='block_user', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='follow',
            field=models.ManyToManyField(related_name='follow_user', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
