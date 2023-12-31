# Generated by Django 5.0 on 2023-12-24 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_danhgiasp_xephang_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danhgiasp',
            name='xepHang',
            field=models.IntegerField(choices=[(2, '★★☆☆☆'), (5, '★★★★★'), (3, '★★★☆☆'), (1, '★☆☆☆☆'), (4, '★★★★☆')], default=None),
        ),
        migrations.AlterField(
            model_name='danhsachdathang',
            name='trangThaiDH',
            field=models.CharField(choices=[('delivered', 'Đang giao hàng'), ('process', 'Đang xử lý'), ('shipped', 'Đang vận chuyển')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='giohang',
            name='trangThaiSP',
            field=models.CharField(choices=[('delivered', 'Đang giao hàng'), ('process', 'Đang xử lý'), ('shipped', 'Đang vận chuyển')], default='processing', max_length=10),
        ),
        migrations.AlterField(
            model_name='sanpham',
            name='trangThaiSP',
            field=models.CharField(choices=[('published', 'Công khai'), ('disabled', 'Xóa'), ('draft', 'Bản nháp'), ('in_revie', 'Xem xét'), ('rejected', 'Từ chối')], default='in_revie', max_length=10),
        ),
    ]
