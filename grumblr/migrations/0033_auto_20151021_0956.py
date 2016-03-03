# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0032_auto_20151020_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='block',
            field=models.ManyToManyField(related_name='blocked_by', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='follow',
            field=models.ManyToManyField(related_name='followed_by', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
