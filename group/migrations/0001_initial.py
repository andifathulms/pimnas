# Generated by Django 4.0.3 on 2022-03-10 23:49

from django.conf import settings
from django.db import migrations, models
import django_editorjs.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('1', 'UKM'), ('2', 'HIMA')], max_length=255)),
                ('about', django_editorjs.fields.EditorJsField()),
                ('achievement', django_editorjs.fields.EditorJsField()),
                ('agenda', django_editorjs.fields.EditorJsField()),
                ('struktur', django_editorjs.fields.EditorJsField()),
                ('admins', models.ManyToManyField(blank=True, related_name='admins', to=settings.AUTH_USER_MODEL)),
                ('pembina', models.ManyToManyField(blank=True, related_name='pembina', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
