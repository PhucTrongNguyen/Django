from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from core.models import SanPham, LoaiSP, NhaCungCap, GioHang, SP_DH, DanhGiaSP, DanhSachDatHang, DiaChi, DanhSachYeuThich
from core.forms import DanhGiaSPForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Count

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.core import serializers

import calendar
from django.db.models.functions import ExtractMonth

# Create your views here.

def index(request):
    #product = SanPham.objects.all()
    #return render(request, "core/index.html")
    #return HttpResponse("hello")
    product = SanPham.objects.filter(sanCo=True, trangThaiSP='published')

    p = Paginator(SanPham.objects.all(), 4)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {
        "product":product,
        "products":products
    }

    return render(request, 'core/index.html', context)

@login_required
def product_list_view(request):
    product = SanPham.objects.filter(trangThaiSP='published')
    number_product = SanPham.objects.filter(trangThaiSP='published')

    p = Paginator(SanPham.objects.all(), 8)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {
        "product":product,
        "products":products,
        "number_product": number_product,
    }

    return render(request, 'core/product-list.html', context)

@login_required
def category_product_list_view(request, maLoai):
    category = LoaiSP.objects.get(maLoai= maLoai)
    product = SanPham.objects.filter(trangThaiSP='published', loaiSP = category)
    number_product = SanPham.objects.filter(trangThaiSP='published', loaiSP = category)

    p = Paginator(product, 8)
    page = request.GET.get('page')
    product = p.get_page(page)

    context = {
        "category":category,
        "product":product,
        "number_product": number_product,
    }
    return render(request, "core/category_product_list.html", context)

@login_required
def vender_list_view(request):
    vender = NhaCungCap.objects.all()
    number_vender = NhaCungCap.objects.all()

    p = Paginator(vender, 4)
    page = request.GET.get('page')
    vender = p.get_page(page)

    context = {
        "vender":vender,
        "number_vender":number_vender
    }
    return render(request, "core/vender-list.html", context)

def vender_detail_view(request, maNCC):
    vender = NhaCungCap.objects.get(maNCC=maNCC)
    product = SanPham.objects.filter(nhaCungCap=vender, trangThaiSP='published')
    number_product = SanPham.objects.filter(nhaCungCap=vender, trangThaiSP='published')

    p = Paginator(product, 4)
    page = request.GET.get('page')
    product = p.get_page(page)

    context = {
        "vender":vender,
        "product":product,
        "number_product": number_product
    }
    return render(request, "core/vender-detail.html", context)

def product_detail_view(request, maSP):
    product = SanPham.objects.get(maSP=maSP)
    products = SanPham.objects.filter(loaiSP = product.loaiSP, trangThaiSP='published').exclude(maSP=maSP)

    reviews = DanhGiaSP.objects.filter(sanPham=product)

    review_form = DanhGiaSPForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = DanhGiaSP.objects.filter(user=request.user.id, sanPham=product).count()

        if user_review_count > 0:
            make_review = False

    p = Paginator(products, 4)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {
        "product":product,
        "products":products,
        "reviews":reviews,
        "review_form":review_form,
        "make_review":make_review
    }

    return render(request, "core/product-detail.html", context)

def ajax_add_review(request, maSP):
    product = SanPham.objects.get(maSP=maSP)
    user = request.user

    review = DanhGiaSP.objects.create(
        user=user,
        sanPham=product,
        danhGia=request.POST['review'],
        xepHang=request.POST['xepHang']
    )

    context = {
        'user':user.username,
        'danhGia':request.POST['review'],
        'xepHang':request.POST['xepHang'],
    }

    return JsonResponse(
        {
            'bool': True,
            'context': context,
        }
    )

@login_required
def search_view(request):
    query = request.GET.get("SP")

    products = SanPham.objects.filter(tenSP__icontains=query)
    number_product = SanPham.objects.filter(tenSP__icontains=query)

    p = Paginator(products, 8)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {
        "products":products,
        "query":query,
        "number_product":number_product
    }
    return render(request, "core/search.html", context)

def filter_product(request):
    venders = request.GET.getlist('vender[]')

    min_gia = request.GET['min_gia']
    max_gia = request.GET['max_gia']

    products = SanPham.objects.filter(trangThaiSP='published').order_by("-maSP").distinct()
    number_product = SanPham.objects.filter(trangThaiSP='published').order_by("-maSP").distinct()

    

    if len(venders) > 0:
        products = products.filter(giaBan__gte = min_gia)
        products = products.filter(giaBan__lte = max_gia)
        products = products.filter(nhaCungCap__maNCC__in=venders).distinct()
        p = Paginator(products, 8)
        page = request.GET.get('page')
        products = p.get_page(page)
    elif len(venders) == 0:
        products = products.filter(giaBan__gte = min_gia)
        products = products.filter(giaBan__lte = max_gia)
        p = Paginator(products, 8)
        page = request.GET.get('page')
        products = p.get_page(page)
    else:
        p = Paginator(SanPham.objects.all(), 8)
        page = request.GET.get('page')
        products = p.get_page(page)

    
    
    data = render_to_string("core/async/product-list.html", {"products":products, "number_product":number_product})
    return JsonResponse({"data": data})

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['maSP'])] = {
        'tenSP': request.GET['tenSP'],
        'soLuong': request.GET['soLuong'],
        'giaBan': request.GET['giaBan'],
        'anhSP': request.GET['anhSP'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['maSP']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['maSP'])]['soLuong'] = int(cart_product[str(request.GET['maSP'])]['soLuong'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})

@login_required
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['soLuong']) * float(item['giaBan'])
        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Giỏ hàng đang trống")
        return redirect("core:index")
    
def delete_item_from_cart(request):
    product_id = str(request.GET['maSP'])
    if "cart_data_obj" in request.session:
        if product_id in request.session["cart_data_obj"]:
            cart_data = request.session["cart_data_obj"]
            del request.session["cart_data_obj"][product_id]
            request.session["cart_data_obj"] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['soLuong']) * float(item['giaBan'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['maSP'])
    product_qty = request.GET['soLuong']

    if "cart_data_obj" in request.session:
        if product_id in request.session["cart_data_obj"]:
            cart_data = request.session["cart_data_obj"]
            cart_data[str(request.GET["maSP"])]["soLuong"] = product_qty
            request.session["cart_data_obj"] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['soLuong']) * float(item['giaBan'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['soLuong']) * int(item['giaBan'])
        
        order = DanhSachDatHang.objects.create(
            user = request.user,
            giaBan = total_amount,
        )

        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['soLuong']) * int(item['giaBan'])

            sp_dh = SP_DH.objects.create(
                datHang = order,
                sanPham = item['tenSP'],
                anhSP = item['anhSP'],
                soLuong = item['soLuong'],
                giaBan = item['giaBan'],
                thanhTien = int(item['soLuong']) * float(item['giaBan']),
            )


    host = request.get_host()
    paypal_dict = {
        'business': "hoangphuc@gmail.com",
        'amount': cart_total_amount,
        'currency_code':'USD',
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial = paypal_dict)

    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for product_id, item in request.session['cart_data_obj'].items():
    #         cart_total_amount += int(item['soLuong']) * float(item['giaBan'])
        
    return render(request, "core/checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'paypal_payment_button': paypal_payment_button, 'cart_total_amount': cart_total_amount})

@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['soLuong']) * float(item['giaBan'])

    return render(request, "core/payment-completed.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders = DanhSachDatHang.objects.filter(user= request.user.id).order_by("-id")
    address = DiaChi.objects.filter(user = request.user)

    order = DanhSachDatHang.objects.annotate(month=ExtractMonth("ngayDH")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    for o in order:
        month.append(calendar.month_name[o['month']])
        total_orders.append(o["count"])

    if request.method == "POST":
        address = request.POST.get("address")

        new_address = DiaChi.objects.create(
            user = request.user,
            diaChi = address
        )
        messages.success(request, "Dia chi da duoc luu")
        return redirect("core:dashboard")

    context = {
        "orders":orders,
        "address": address,
        "order": order,
        "month": month,
        "total_orders": total_orders
    }

    return render(request, 'core/dashboard.html', context)

def order_detail(request, id):
    order = DanhSachDatHang.objects.get(user = request.user.id, id = id)
    products = SP_DH.objects.filter(datHang = order)

    context = {
        "products": products,
    }
    return render(request, 'core/order-detail.html', context)

@login_required
def wishlist_view(request):
    wishlist = DanhSachYeuThich.objects.all()
    context = {
        'wishlist': wishlist,
    }

    return render(request, "core/wishlist.html", context)

def add_to_wishlist(request):
    id = request.GET["maSP"]
    product = SanPham.objects.get(maSP= id)

    context = {

    }

    wishlist_count = DanhSachYeuThich.objects.filter(sanPham = product, user = request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True,
        }
    else:
        new_wishlist = DanhSachYeuThich.objects.create(
            sanPham = product,
            user = request.user,
        )
        context = {
            "bool": True,
        }

    return JsonResponse(context)

def remove_wishlist(request):
    pid = request.GET['maSP']
    wishlist = DanhSachYeuThich.objects.filter(user = request.user)    
    wishlist_d = DanhSachYeuThich.objects.get(id = pid)
    delete_product = wishlist_d.delete()

    context = {
        "bool": True,
        "wishlist": wishlist,
    }

    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data": data, "wishlist":wishlist_json})

def remove_orders(request):
    oid = request.GET["oid"]
    orders = DanhSachDatHang.objects.filter(user = request.user.id).order_by("-id")
    orders_d = DanhSachDatHang.objects.get(id = oid)
    delete_order = orders_d.delete()

    context = {
        "bool": True,
        "orders": orders,
    }

    orders_json = serializers.serialize('json', orders)
    data = render_to_string("core/async/order-list.html", context)
    return JsonResponse({"data": data, "orders": orders_json})

def make_address_default(request):
    id = request.GET["id"]
    DiaChi.objects.update(trangThai= False)
    DiaChi.objects.filter(id= id).update(trangThai = True)
    return JsonResponse({"boolean": True})
