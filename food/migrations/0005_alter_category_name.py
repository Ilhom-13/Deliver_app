from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('food', '0004_alter_category_user')]
    operations = [
       migrations.AlterField(model_name='category',
       name='name',
       field=models.CharField(max_length=150))]
