# Generated by Django 3.2.3 on 2021-05-21 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calliope_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200, verbose_name='body')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created datetime')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='updated datetime')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'bss',
                'verbose_name_plural': 'bss',
            },
        ),
    ]