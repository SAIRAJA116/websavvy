# Generated by Django 3.2.9 on 2021-11-15 11:11

import App.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_auto_20211114_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_event',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('icon', models.ImageField(upload_to=App.models.get_eventlogo_path)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='App.post')),
            ],
        ),
    ]
