# Generated by Django 4.1.7 on 2023-03-16 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=1000)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='politicians.city')),
            ],
        ),
        migrations.RemoveField(
            model_name='issue',
            name='politician',
        ),
        migrations.AlterField(
            model_name='politician',
            name='biography',
            field=models.CharField(max_length=10000),
        ),
        migrations.DeleteModel(
            name='Committee',
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
    ]
