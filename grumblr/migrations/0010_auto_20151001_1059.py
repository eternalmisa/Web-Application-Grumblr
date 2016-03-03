# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0009_auto_20150930_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=42)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='dislike',
            field=models.ManyToManyField(related_name='disliked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='like',
            field=models.ManyToManyField(related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userinformation',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userinformation',
            name='follows',
            field=models.ManyToManyField(related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userinformation',
            name='short_bio',
            field=models.CharField(default=b'', max_length=420),
        ),
        migrations.AddField(
            model_name='comment',
            name='posted_message',
            field=models.ForeignKey(related_name='comments', to='grumblr.Message'),
        ),
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
