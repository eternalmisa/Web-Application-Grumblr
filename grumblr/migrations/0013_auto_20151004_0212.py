# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0012_auto_20151004_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='avatar',
            field=models.ImageField(default=b'default.jpg', upload_to=b'grumblr-avatar'),
        ),
    ]
