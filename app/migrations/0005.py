from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="comment_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="likes_count",
            field=models.IntegerField(default=0),
        ),
    ]
