# Generated by Django 4.0.5 on 2022-06-19 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_locations_options_appointments'),
    ]

    operations = [
        migrations.CreateModel(
            name='cut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='appointments',
            name='cut',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.cut'),
        ),
    ]
