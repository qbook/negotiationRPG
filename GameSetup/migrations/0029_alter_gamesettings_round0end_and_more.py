# Generated by Django 4.2.5 on 2023-11-23 23:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameSetup', '0028_alter_gamesettings_round0end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesettings',
            name='round0End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 24, 4, 59, 13, 894878, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round0Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 24, 0, 59, 13, 894837, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 4, 59, 13, 894914, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 30, 23, 59, 13, 894887, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 8, 4, 59, 13, 894946, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 7, 23, 59, 13, 894920, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 4, 59, 13, 894974, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 23, 59, 13, 894952, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 22, 4, 59, 13, 895005, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 21, 23, 59, 13, 894980, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 29, 4, 59, 13, 895034, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 28, 23, 59, 13, 895011, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 4, 59, 13, 895062, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 23, 59, 13, 895040, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 12, 4, 59, 13, 895089, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 11, 23, 59, 13, 895067, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 4, 59, 13, 895114, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 23, 59, 13, 895094, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 4, 59, 13, 895141, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 25, 23, 59, 13, 895119, tzinfo=datetime.timezone.utc)),
        ),
    ]
