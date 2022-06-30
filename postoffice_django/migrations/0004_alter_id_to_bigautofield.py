from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postoffice_django', '0003_set_json_encoder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishingerror',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
