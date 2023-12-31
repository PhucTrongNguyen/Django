from django.urls import path, include
from core.views import index, product_list_view, category_product_list_view, vender_list_view, vender_detail_view, product_detail_view, ajax_add_review, search_view, filter_product, add_to_cart, cart_view, delete_item_from_cart, update_cart, checkout_view, payment_completed_view, payment_failed_view, customer_dashboard, order_detail, wishlist_view, add_to_wishlist, remove_wishlist, make_address_default, remove_orders

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("category/<maLoai>", category_product_list_view, name="category_product_list"),
    path("vender/", vender_list_view, name="vender-list"),
    path("vender/<maNCC>", vender_detail_view, name="vender-detail"),
    path("product/<maSP>", product_detail_view, name="product-detail"),
    path("ajax-add-review/<maSP>", ajax_add_review, name="ajax-add-review"),
    path("search/", search_view, name="search"),
    path("filter-products/", filter_product, name="filter-product"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("cart/", cart_view, name="cart"),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path("update-cart/", update_cart, name="update-cart"),
    path("checkout/", checkout_view, name="checkout"),
    path("paypal/", include("paypal.standard.ipn.urls")),
    path('payment-completed/', payment_completed_view, name="payment-completed"),
    path('payment-failed/', payment_failed_view, name="payment-failed"),
    path('dashboard/', customer_dashboard, name="dashboard"),
    path('dashboard/order/<int:id>', order_detail, name="order-detail"),
    path('wishlist/', wishlist_view, name="wishlist"),
    path('add-to-wishlist/', add_to_wishlist, name="add-to-wishlist"),
    path('remove-from-wishlist/', remove_wishlist, name="remove-from-wishlist"),
    path('make-default-address/', make_address_default, name="make-default-address"),
    path('remove-orders/', remove_orders, name="remove-orders")
]
