# Generated by Django 3.2 on 2022-08-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0003_achievement_achievementcat'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='achievements',
            field=models.ManyToManyField(through='cats.AchievementCat', to='cats.Achievement'),
        ),
    ]
