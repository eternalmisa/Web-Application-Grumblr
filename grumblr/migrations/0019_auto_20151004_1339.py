# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0018_auto_20151004_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='img',
            field=models.ImageField(upload_to=b'picture', blank=True),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='avatar',
            field=models.ImageField(default=b'avatar/default.jpg', upload_to=b'avatar'),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='phoneNum',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
