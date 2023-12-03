# Generated by Django 4.2.5 on 2023-11-23 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_surveysection_code_surveysection_code_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyquestion',
            old_name='order',
            new_name='question_number',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='question',
        ),
        migrations.AddField(
            model_name='userresponse',
            name='question_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresponse',
            name='section_code',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='surveysection',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
