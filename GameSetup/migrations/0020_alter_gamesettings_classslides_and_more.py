# Generated by Django 4.2.5 on 2023-11-18 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameSetup', '0019_alter_gamesettings_classslides_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesettings',
            name='classSlides',
            field=models.CharField(default='https://bit.ly/39NbwJe', help_text='Class Slides', max_length=1000),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='eBook',
            field=models.CharField(default='https://drive.google.com/file/d/17TXHyR-YXaDh6Wz_bua9hTIe6eHi0NS6/view?usp=sharing', help_text='Class eBook', max_length=1000),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round0End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 18, 18, 53, 6, 218330, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round0Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 18, 14, 53, 6, 218288, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 18, 53, 6, 218442, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 13, 53, 6, 218338, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 18, 53, 6, 218480, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 13, 53, 6, 218451, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 18, 53, 6, 218509, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 13, 53, 6, 218487, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 18, 53, 6, 218540, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 13, 53, 6, 218515, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 23, 18, 53, 6, 218566, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 23, 13, 53, 6, 218546, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 18, 53, 6, 218594, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 13, 53, 6, 218572, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 6, 18, 53, 6, 218621, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 6, 13, 53, 6, 218600, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 18, 53, 6, 218650, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 13, 53, 6, 218627, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9End',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 20, 18, 53, 6, 218677, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9Start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 20, 13, 53, 6, 218655, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='userGuide',
            field=models.CharField(default='https://docs.google.com/document/d/1KCIf7SJVeFeMZ05ecCmT1Wey9Z0alWUn83Tr3GjNzYU/edit?usp=drive_link', help_text='User Guide', max_length=1000),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='videoLectures',
            field=models.CharField(default='https://bit.ly/3kMXnlM', help_text='Video Lectures', max_length=1000),
        ),
    ]
