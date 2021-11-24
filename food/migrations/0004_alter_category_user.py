from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ('food', '0003_item_num_of_sold')]
    operations = [
    migrations.AlterField(model_name='category',
                       name='user',
                       field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL))
                    ]
