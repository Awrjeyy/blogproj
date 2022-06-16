# Generated by Django 4.0.5 on 2022-06-15 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='following',
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('another_email', models.ManyToManyField(related_name='another_email', to=settings.AUTH_USER_MODEL)),
                ('currentemail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]