# Generated by Django 3.2.3 on 2021-05-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calliope_web', '0003_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
    ]