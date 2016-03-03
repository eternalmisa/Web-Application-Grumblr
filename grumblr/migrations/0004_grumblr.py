# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0003_auto_20150921_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grumblr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=50)),
                ('school', models.CharField(max_length=50)),
                ('phoneNum', models.IntegerField(max_length=20)),
                ('photoURL', models.CharField(max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
