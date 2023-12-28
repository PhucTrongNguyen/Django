from django.contrib import admin
from core.models import SanPham, LoaiSP, NhaCungCap, GioHang, SP_DH, DanhGiaSP, DanhSachDatHang, DiaChi, ThongTinSP, DanhSachYeuThich

class SanPhamAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenSP', 'anhSP', 'giaBan', 'sanCo', 'trangThaiSP']

class ThongTinSPAdmin(admin.ModelAdmin):
    list_display = ['sanPham', 'tenThuongHieu', 'chatLieu', 'kieuDang', 'tgBaoHanh']

class LoaiSPAdmin(admin.ModelAdmin):
    list_display = ['tenLoai']

class NhaCungCapAdmin(admin.ModelAdmin):
    list_display = ['tenNCC']

class GioHangAdmin(admin.ModelAdmin):
    list_display = ['user', 'giaBan', 'trangThaiThanhToan', 'ngayDatHang', 'trangThaiSP']

class SP_DHAdmin(admin.ModelAdmin):
    list_display = ['datHang', 'sanPham', 'anhSP', 'soLuong', 'giaBan', 'thanhTien']

class DanhGiaSPAdmin(admin.ModelAdmin):
    list_display = ['user', 'sanPham', 'danhGia', 'xepHang']

class DanhSachDatHangAdmin(admin.ModelAdmin):
    list_editable = ['trangThaiDH', 'trangThaiThanhToan']
    list_display = ['user', 'giaBan', 'trangThaiDH', 'trangThaiThanhToan', 'ngayDH']

class DiaChiAdmin(admin.ModelAdmin):
    list_display = ['user', 'diaChi', 'trangThai']

class DanhSachYeuThichAdmin(admin.ModelAdmin):
    list_display = ['user', 'sanPham', 'ngayThem']

admin.site.register(SanPham, SanPhamAdmin)
admin.site.register(LoaiSP, LoaiSPAdmin)
admin.site.register(NhaCungCap, NhaCungCapAdmin)
admin.site.register(GioHang, GioHangAdmin)
admin.site.register(SP_DH, SP_DHAdmin)
admin.site.register(DanhGiaSP, DanhGiaSPAdmin)
admin.site.register(DanhSachDatHang, DanhSachDatHangAdmin)
admin.site.register(DiaChi, DiaChiAdmin)
admin.site.register(ThongTinSP, ThongTinSPAdmin)
admin.site.register(DanhSachYeuThich, DanhSachYeuThichAdmin)