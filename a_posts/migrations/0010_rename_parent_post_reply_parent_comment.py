# Generated by Django 5.0.6 on 2024-07-08 22:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("a_posts", "0009_reply"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reply",
            old_name="parent_post",
            new_name="parent_comment",
        ),
    ]
