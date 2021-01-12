# Generated by Django 3.1.3 on 2021-01-07 22:21

import app.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('domaine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom', models.CharField(default='', max_length=100)),
                ('lien', models.CharField(default='', max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=app.models.upload_path, verbose_name='avatar')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
                ('domaines', models.ManyToManyField(to='domaine.Domaine')),
            ],
            options={
                'ordering': ['create_at'],
            },
        ),
    ]