# Generated by Django 3.1.7 on 2021-04-04 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='useremail',
            field=models.CharField(max_length=128),
        ),
    ]
