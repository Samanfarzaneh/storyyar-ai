# Generated by Django 5.1.4 on 2025-01-12 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='output_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/output_images/'),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='source_image',
            field=models.ImageField(upload_to='media/source_images/'),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='target_image',
            field=models.ImageField(upload_to='media/target_images/'),
        ),
    ]
