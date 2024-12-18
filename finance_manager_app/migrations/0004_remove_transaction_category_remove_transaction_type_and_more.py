# Generated by Django 4.2.16 on 2024-11-26 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_manager_app', '0003_remove_transaction_title_transaction_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='category_expense',
            field=models.CharField(blank=True, choices=[('mandatory', 'Обязательные расходы'), ('food', 'Продукты'), ('car', 'Автомобиль'), ('entertainment', 'Развлечения'), ('household', 'Товары для дома'), ('selfcare', 'Забота о себе'), ('education', 'Образование'), ('miscellaneous', 'Разное')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category_income',
            field=models.CharField(blank=True, choices=[('salary', 'Зарплата'), ('other', 'Другие источники')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('income', 'Доход'), ('expense', 'Расход')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
