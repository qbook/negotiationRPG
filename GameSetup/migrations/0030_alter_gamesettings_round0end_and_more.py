# Generated by Django 4.2.5 on 2023-11-24 04:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameSetup', '0029_alter_gamesettings_round0end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesettings',
            name='round0End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 24, 9, 2, 5, 553049, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round0Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 24, 5, 2, 5, 553006, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 9, 2, 5, 553087, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 4, 2, 5, 553058, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 8, 9, 2, 5, 553117, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 8, 4, 2, 5, 553093, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 9, 2, 5, 553143, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 4, 2, 5, 553122, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 22, 9, 2, 5, 553172, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 22, 4, 2, 5, 553149, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 29, 9, 2, 5, 553200, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 29, 4, 2, 5, 553177, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 9, 2, 5, 553226, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 4, 2, 5, 553205, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 12, 9, 2, 5, 553253, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 12, 4, 2, 5, 553231, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 9, 2, 5, 553278, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 4, 2, 5, 553258, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 9, 2, 5, 553304, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 4, 2, 5, 553282, tzinfo=datetime.timezone.utc)),
        ),
    ]
