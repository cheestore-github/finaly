# Generated by Django 3.2.15 on 2022-09-15 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.CharField(max_length=50, verbose_name='کد ردیابی تراکنش')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bankinfotocustomuser', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'db_table': 'transfer',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_accept', models.BooleanField(blank=True, null=True)),
                ('rule_deny', models.BooleanField(blank=True, null=True)),
                ('later_read', models.BooleanField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ruletocustomuser', to=settings.AUTH_USER_MODEL, verbose_name='نام کاربر')),
            ],
            options={
                'db_table': 'rule',
            },
        ),
        migrations.CreateModel(
            name='AgentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50, verbose_name='تلفن ثابت')),
                ('birth_year', models.CharField(max_length=50, verbose_name='سال تولد')),
                ('residence_city', models.CharField(max_length=50, verbose_name='شهر محل سکونت')),
                ('agency_city', models.CharField(max_length=50, verbose_name='شهر مورد تقاضا برای نمایندگی')),
                ('job_history', models.TextField(verbose_name='سوابق شغلی')),
                ('last_collab', models.CharField(max_length=50, verbose_name='مدت زمان همکاری در آخرین تجربه شغلی')),
                ('schooling', models.CharField(max_length=50, verbose_name='میزان تحصیلات')),
                ('social_media_skills', models.TextField(max_length=50, verbose_name='مهارت های فضای مجازی')),
                ('job_space', models.TextField(max_length=50, verbose_name='متراژ و نوع مالکیت فضای کار')),
                ('reagent', models.CharField(max_length=50, verbose_name='معرف')),
                ('familiarity_with_us', models.CharField(choices=[('google', 'جستجو در اینترنت'), ('instagram', 'اینستاگرام'), ('telegram', 'تلگرام'), ('friends', 'دوستان و آشنایان'), ('others', 'سایر')], max_length=50, verbose_name='از چه طریق با مجموعه ما آشنا شدید؟')),
                ('plunge_case', models.CharField(max_length=50, verbose_name='وضعیت اشتغال')),
                ('profational_skills', models.TextField(max_length=50, verbose_name='مهارت های حرفه ای')),
                ('languages', models.TextField(max_length=50, verbose_name='میزان آشنایی شما با زبان انگلیسی یا سایر زبان ها')),
                ('favorites', models.TextField(max_length=50, verbose_name='مزایای شغلی موردعلاقه')),
                ('cv', models.FileField(upload_to='agent_cv/', verbose_name='آپلود فایل رزومه')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'agent',
            },
        ),
    ]
