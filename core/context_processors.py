from core.models import LoaiSP, DiaChi, NhaCungCap, SanPham, DanhSachYeuThich
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    loaiSP = LoaiSP.objects.all()
    try:
        diaChi = DiaChi.objects.get(user=request.user.id, trangThai = True)
    except:
        diaChi = None

    min_max_gia = SanPham.objects.aggregate(Min("giaBan"), Max("giaBan"))

    try:
        wishlist = DanhSachYeuThich.objects.filter(user = request.user)
    except:
        wishlist = 0

    nhaCungCap = NhaCungCap.objects.all()

    return {
        'category_product_list': loaiSP,
        'address': diaChi,
        'vender': nhaCungCap,
        'min_max_gia': min_max_gia,
        'wishlist': wishlist,
    }
