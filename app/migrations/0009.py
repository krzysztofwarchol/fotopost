from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008"),
    ]

    operations = [
        migrations.RenameField(
            model_name="follower",
            old_name="follower",
            new_name="followers",
        ),
    ]
