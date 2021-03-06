# Generated by Django 2.0.3 on 2018-04-10 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_auto_20180409_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
