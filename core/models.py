# from email.policy import default
# from pyexpat import model
# from unicodedata import decimal
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = {
    ('processing', 'Đang xử lý'),
    ('shipped', 'Đang vận chuyển'),
    ('delivered', 'Đang giao hàng')
}


STATUS = {
    ('draft', 'Bản nháp'),
    ('disabled', 'Xóa'),
    ('rejected', 'Từ chối'),
    ('in_revie', 'Xem xét'),
    ('published', 'Công khai')
}

RATING = {
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
}


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class LoaiSP(models.Model):
    maLoai = ShortUUIDField(unique=True, length=10, max_length=30, prefix="L", alphabet="abcdefgh12345")
    tenLoai = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "LoaiSPs"
    
    def __str__(self):
        return self.tenLoai

class NhaCungCap(models.Model):
    maNCC = ShortUUIDField(unique=True, length=10, max_length=30, prefix="KH", alphabet="abcdefgh12345")
    
    tenNCC = models.CharField(max_length=100)
    #moTa = models.TextField(null=True, blank=True)
    moTa = RichTextUploadingField(null= True, blank= True)

    diaChi = models.CharField(max_length=100, default="123 Main Street.")
    lienHe = models.CharField(max_length=100, default="+123 (456) 789")
    tGPhanHoi = models.CharField(max_length=100, default="100")
    tGVanChuyen = models.CharField(max_length=100, default="100")
    danhGia = models.CharField(max_length=100, default="100")
    ngayQuayLai = models.CharField(max_length=100, default="100")
    thoiHanBaoHanh = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "NhaCungCaps"
    
    def __str__(self):
        return self.tenNCC

class SanPham(models.Model):
    maSP = ShortUUIDField(unique=True, length=10, max_length=30, prefix="SP", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    tenSP = models.CharField(max_length=100)
    anhSP = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    #moTa = models.TextField(null=True, blank=True)
    moTa = RichTextUploadingField(null= True, blank= True)

    giaBan = models.DecimalField(max_digits=99999999999999, decimal_places=0, default="10000")
    giaCu = models.DecimalField(max_digits=99999999999999, decimal_places=0, default="10000")

    trangThaiSP = models.CharField(choices=STATUS, max_length=10, default="in_revie")
    sanCo = models.BooleanField(default=True)

    loaiSP = models.ForeignKey(LoaiSP, on_delete=models.SET_NULL, null=True)
    nhaCungCap = models.ForeignKey(NhaCungCap, on_delete=models.SET_NULL, null=True, related_name="product")

    class Meta:
        verbose_name_plural = "SanPhams"
    
    def product_image(self):
        return mark_safe('<img src="~%s" width="50" height="50" />' % (self.anhSP.url))

    def __str__(self):
        return self.tenSP
    
    def get_precentage(self):
        new_price = (self.giaBan / self.giaCu) * 100
        return new_price

class ThongTinSP(models.Model):
    maTT = ShortUUIDField(unique=True, length=10, max_length=30, prefix="TT", alphabet="abcdefgh12345")
    sanPham = models.ForeignKey(SanPham, on_delete= models.SET_NULL, null=True)
    tenThuongHieu = models.CharField(max_length=100)
    chatLieu = models.CharField(max_length=100)
    kieuDang = models.CharField(max_length=100)
    tgBaoHanh = models.CharField(max_length=100, default="6")

    class Meta:
        verbose_name_plural = "ThongTinSPs"

    def __str__(self):
        return self.sanPham.tenSP


class GioHang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    giaBan = models.DecimalField(max_digits=99999999999999, decimal_places=0, default="10000")
    trangThaiThanhToan = models.BooleanField(default=False)
    ngayDatHang = models.DateTimeField(auto_now_add=True)
    trangThaiSP = models.CharField(choices=STATUS_CHOICE, max_length=10, default="processing")

    class Meta:
        verbose_name_plural = "GioHangs"
     
class DanhGiaSP(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sanPham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True, related_name="reviews")
    danhGia = models.TextField()
    xepHang = models.IntegerField(choices=RATING, default=None)
    ngayDG = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "DanhGiaSPs"
    
    def __str__(self):
        return self.sanPham.tenSP
    
    def get_rating(self):
        return self.xepHang
    
class DanhSachDatHang(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #sanPham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)
    giaBan = models.DecimalField(max_digits=99999999999999, decimal_places=0, default="10000")
    trangThaiDH = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    trangThaiThanhToan = models.BooleanField(default=False)
    ngayDH = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "DanhSachDatHangs"
    
class SP_DH(models.Model):
    datHang = models.ForeignKey(DanhSachDatHang, on_delete=models.CASCADE)
    trangThaiSP = models.CharField(max_length=100)
    sanPham = models.CharField(max_length=100)
    anhSP = models.CharField(max_length=100)
    soLuong = models.IntegerField(default=0)
    giaBan = models.DecimalField(max_digits=99999999999999, decimal_places=0, default="10000")
    thanhTien = models.DecimalField(max_digits=99999999999999, decimal_places=0, default="10000")

    class Meta:
        verbose_name_plural = "SP_DHs"
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.anhSP))
   

class DiaChi(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    diaChi = models.CharField(max_length=100, null=True)
    trangThai = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "DiaChis"

class DanhSachYeuThich(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    sanPham = models.ForeignKey(SanPham, on_delete= models.SET_NULL, null= True)
    ngayThem = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name_plural = "DanhSachYeuThichs"
    
    def __str__(self):
        return self.sanPham.tenSP
