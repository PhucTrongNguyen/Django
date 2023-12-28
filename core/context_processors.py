from core.models import LoaiSP, DiaChi, NhaCungCap, SanPham, DanhSachYeuThich
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    loaiSP = LoaiSP.objects.all()
    if request.user.is_authenticated:
        diaChi = DiaChi.objects.get(user=request.user.id, trangThai = True)
    else:
        diaChi = None

    min_max_gia = SanPham.objects.aggregate(Min("giaBan"), Max("giaBan"))

    try:
        wishlist = DanhSachYeuThich.objects.filter(user = request.user)
    except:
        messages.warning(request, "Bạn cần phải đăng nhập trước khi thêm sản phẩm vào danh sách yêu thích")
        wishlist = 0

    nhaCungCap = NhaCungCap.objects.all()

    return {
        'category_product_list': loaiSP,
        'address': diaChi,
        'vender': nhaCungCap,
        'min_max_gia': min_max_gia,
        'wishlist': wishlist,
    }