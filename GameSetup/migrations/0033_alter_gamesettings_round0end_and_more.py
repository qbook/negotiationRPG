# Generated by Django 4.2.5 on 2023-11-25 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameSetup', '0032_alter_gamesettings_round0end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesettings',
            name='round0End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 12, 31, 49, 713461, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round0Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 8, 31, 49, 713411, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 31, 49, 713501, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 7, 31, 49, 713471, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 12, 31, 49, 713538, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 7, 31, 49, 713508, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 12, 31, 49, 713570, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 7, 31, 49, 713544, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 23, 12, 31, 49, 713603, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 23, 7, 31, 49, 713577, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 12, 31, 49, 713636, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 7, 31, 49, 713609, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 6, 12, 31, 49, 713666, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 6, 7, 31, 49, 713642, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 12, 31, 49, 713698, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 7, 31, 49, 713673, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 20, 12, 31, 49, 713726, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 20, 7, 31, 49, 713704, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 27, 12, 31, 49, 713758, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 27, 7, 31, 49, 713733, tzinfo=datetime.timezone.utc)),
        ),
    ]
