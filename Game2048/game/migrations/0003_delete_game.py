# Generated by Django 5.1.3 on 2024-12-03 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_best_score_alter_game_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Game',
        ),
    ]
