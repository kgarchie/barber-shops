# Generated by Django 4.0.5 on 2022-06-19 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name_plural': 'Locations'},
        ),
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cut', models.CharField(max_length=20)),
                ('dye', models.BooleanField()),
                ('sth', models.TextField(blank=True, null=True)),
                ('barber', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.barber')),
                ('locale', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.locations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
