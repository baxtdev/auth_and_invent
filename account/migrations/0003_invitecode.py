# Generated by Django 4.1.7 on 2024-04-22 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_eamil'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, unique=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invited_code', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, null=True, related_name='invited_users', to=settings.AUTH_USER_MODEL, verbose_name='Приглашенные пользователи')),
            ],
        ),
    ]