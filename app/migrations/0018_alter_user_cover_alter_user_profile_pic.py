from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0017_alter_comment_id_alter_follower_id_alter_post_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="cover",
            field=models.ImageField(blank=True, upload_to="covers/"),
        ),
        migrations.AlterField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(upload_to="profile_pic/"),
        ),
    ]
