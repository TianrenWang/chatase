# Generated by Django 4.2.7 on 2023-11-30 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_conversation_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPTOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectiveInput', models.CharField()),
                ('objectiveOutput', models.CharField()),
                ('emotionInput', models.CharField()),
                ('emotionOutput', models.CharField()),
                ('behaviourOutput', models.CharField()),
                ('gptInput', models.JSONField()),
                ('gptOutput', models.CharField()),
                ('extractionInput', models.CharField()),
                ('extractionOutput', models.CharField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('message', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gptoutput', to='chatbot.message')),
            ],
        ),
    ]
