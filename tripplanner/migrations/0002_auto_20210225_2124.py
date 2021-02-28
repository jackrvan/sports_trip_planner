# Generated by Django 3.1.6 on 2021-02-26 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tripplanner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhlteam',
            name='team_name',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_country', models.CharField(choices=[('US', 'USA'), ('CA', 'Canada')], max_length=2)),
                ('starting_province', models.CharField(max_length=50)),
                ('starting_city', models.CharField(max_length=50)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tripplanner.nhlteam')),
            ],
        ),
    ]
