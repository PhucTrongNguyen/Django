# Generated by Django 5.0 on 2023-12-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_danhgiasp_xephang_alter_giohang_trangthaisp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danhgiasp',
            name='xepHang',
            field=models.IntegerField(choices=[(3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★'), (2, '★★☆☆☆'), (1, '★☆☆☆☆')], default=None),
        ),
        migrations.AlterField(
            model_name='sanpham',
            name='trangThaiSP',
            field=models.CharField(choices=[('rejected', 'Từ chối'), ('in_revie', 'Xem xét'), ('disabled', 'Xóa'), ('published', 'Công khai'), ('draft', 'Bản nháp')], default='in_revie', max_length=10),
        ),
    ]
