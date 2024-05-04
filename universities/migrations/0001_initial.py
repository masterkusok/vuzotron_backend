# Generated by Django 4.2.11 on 2024-05-04 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('specialities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('auto_update', models.BooleanField(default=True)),
                ('short_name', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('sys_guid', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.TextField()),
                ('specialities', models.ManyToManyField(to='specialities.speciality')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
