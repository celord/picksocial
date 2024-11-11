# Generated by Django 5.0.6 on 2024-07-09 00:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a_posts", "0010_rename_parent_post_reply_parent_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reply",
            name="parent_comment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="a_posts.comment",
            ),
        ),
    ]
