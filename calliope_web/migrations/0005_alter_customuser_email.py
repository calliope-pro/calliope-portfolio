# Generated by Django 3.2.3 on 2021-05-23 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calliope_web', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
