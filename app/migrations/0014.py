from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(default="no_pic.png", upload_to="profile_pic/"),
        ),
    ]
