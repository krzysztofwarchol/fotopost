from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(upload_to="profile_pic/"),
        ),
    ]
