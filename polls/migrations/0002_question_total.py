# Generated by Django 2.2.6 on 2019-10-14 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
