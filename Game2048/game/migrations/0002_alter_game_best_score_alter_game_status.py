# Generated by Django 5.1.3 on 2024-12-03 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='best_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(default='In Progress', max_length=20),
        ),
    ]
