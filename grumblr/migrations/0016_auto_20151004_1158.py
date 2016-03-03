# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0015_auto_20151004_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='avatar',
            field=models.ImageField(upload_to=b'avatar'),
        ),
    ]
