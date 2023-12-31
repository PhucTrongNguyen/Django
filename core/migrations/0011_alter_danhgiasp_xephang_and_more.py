# Generated by Django 5.0 on 2023-12-24 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_danhsachdathang_trangthaithanhtoan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danhgiasp',
            name='xepHang',
            field=models.IntegerField(choices=[(4, '★★★★☆'), (3, '★★★☆☆'), (1, '★☆☆☆☆'), (2, '★★☆☆☆'), (5, '★★★★★')], default=None),
        ),
        migrations.AlterField(
            model_name='danhsachdathang',
            name='trangThaiDH',
            field=models.CharField(choices=[('process', 'Đang xử lý'), ('delivered', 'Đang giao hàng'), ('shipped', 'Đang vận chuyển')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='giohang',
            name='trangThaiSP',
            field=models.CharField(choices=[('process', 'Đang xử lý'), ('delivered', 'Đang giao hàng'), ('shipped', 'Đang vận chuyển')], default='processing', max_length=10),
        ),
        migrations.AlterField(
            model_name='sanpham',
            name='trangThaiSP',
            field=models.CharField(choices=[('draft', 'Bản nháp'), ('disabled', 'Xóa'), ('published', 'Công khai'), ('rejected', 'Từ chối'), ('in_revie', 'Xem xét')], default='in_revie', max_length=10),
        ),
        migrations.CreateModel(
            name='SP_DH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trangThaiSP', models.CharField(max_length=100)),
                ('sanPham', models.CharField(max_length=100)),
                ('anhSP', models.CharField(max_length=100)),
                ('soLuong', models.IntegerField(default=0)),
                ('giaBan', models.DecimalField(decimal_places=0, default='10000', max_digits=99999999999999)),
                ('thanhTien', models.DecimalField(decimal_places=0, default='10000', max_digits=99999999999999)),
                ('datHang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.danhsachdathang')),
            ],
            options={
                'verbose_name_plural': 'SP_DHs',
            },
        ),
        migrations.DeleteModel(
            name='SP_GH',
        ),
    ]
