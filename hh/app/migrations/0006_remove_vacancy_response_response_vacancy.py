# Generated by Django 4.2.16 on 2024-09-09 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_vacancy_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='response',
        ),
        migrations.AddField(
            model_name='response',
            name='vacancy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.vacancy'),
        ),
    ]
