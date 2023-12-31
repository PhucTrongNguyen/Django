const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

$("#comment-form").submit(function(e) {
    e.preventDefault();

    let dt = new Date()
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: 'json',

        success: function(response){
            console.log("Correct");

            if (response.bool == true){
                $("#review-res").html("Đánh giá đã thêm thành công")
                $(".hide-comment").hide()
                $(".add-review").hide()

                let _html = '<div class="border row">'
                    _html += '<div class="col-2 d-flex align-items-center">'
                    _html += '<p>' + response.context.user +'</p>'
                    _html += '</div>'
                    _html += '<div class="col-10">'
                    _html += '<div class="d-flex justify-content-between">'
                    _html += '<span>' + time + '</span>'
                    _html += '<span class="d-flex align-items-center">'
                    _html += '<div class="d-flex">'

                    for(let i = 1; i < response.context.xepHang; i++){
                        _html += '<i class="fa-solid fa-star"></i>'
                    }

                    _html += '</div>'
                    _html += '</span>'
                    _html += '</div>'
                    _html += '<p>' + response.context.danhGia + '</p>'
                    _html += '</div>'
                    _html += '</div>'
                
                $(".comment-list").prepend(_html)
            }
           
        }
    });
})

$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        // console.log("Check")

        let filter_object = {}

        let min_gia = $("#max_price").attr("min")
        let max_gia = $("#max_price").val()

        filter_object.min_gia = min_gia
        filter_object.max_gia = max_gia

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            // console.log("Filter value is: ", filter_value);
            // console.log("Filter key is: ", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter= '+ filter_key +']:checked')).map(function(element){
                return element.value
            })
            console.log("Filter object is: ", filter_object)

            $.ajax({
                url: '/filter-products',
                data: filter_object,
                dataType: 'json',
                beforeSend: function(){
                    console.log("Sending data ");
                },
                success: function(response){
                    console.log(response);
                    console.log("Success");
                    $("#filtered-product").html(response.data)
                }
            })
        })
    })

    $(".delete-product").on("click", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product id: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "maSP": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-item-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

    $(".update-product").on("click", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()
    
        console.log("Product id: ", product_id);
        console.log("Product qty: ", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "maSP": product_id,
                "soLuong": product_quantity
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-item-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    
    })

    //Them vao gio hang o home page
    $(".add-to-cart-btn").on("click", function(e){
        e.preventDefault();

        let this_val = $(this);
        let index = this_val.attr("data-index");

        let quantity = $(".product-quantity-" + index).val();
        let product_title = $(".product-title-" + index).val();
        let product_id = $(".product-id-" + index).val();
        let product_price = $(".current-product-price-"+ index).val();
        let product_pid = $(".product-pid-" + index).val();
        let product_image = $(".product-image-" + index).val();

        console.log("quantity: ", quantity);
        console.log("product_title: ", product_title);
        console.log("product_id: ", product_id);
        console.log("product_price: ", product_price);
        console.log("Current Element:", this_val);
        console.log("product_pid: ", product_pid);
        console.log("product_image: ", product_image);
        console.log("index: ", index);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'maSP': product_id,
                'soLuong': quantity,
                'tenSP': product_title,
                'giaBan': product_price,
                'anhSP': product_image,
                'pid': product_pid,
            },
            dataType: 'json',
            beforeSend: function() {
                console.log("Đang thêm vào giỏ hàng");
            },
            success: function(response){
                this_val.html('<i class="fa-solid fa-check"></i>');
                console.log("Đã thêm vào giỏ hàng");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    });

    $("#max_price").on("blur", function(){
        let min_gia = $(this).attr("min");
        let max_gia = $(this).attr("max");
        let gia_hientai = $(this).val();

        console.log("Value current is: ", gia_hientai);
        console.log("Value min is: ", min_gia);
        console.log("Value max is: ", max_gia);

        if (gia_hientai < parseInt(min_gia) || gia_hientai > parseInt(max_gia)) {
            //console.log("Error");

            min_gia = Math.round(min_gia * 100) / 100
            max_gia = Math.round(max_gia * 100) / 100
            
            // console.log("Max price is: ", max_gia)
            // console.log("Min price is: ", min_gia)

            alert("Giá phải từ " + min_gia + " đến " + max_gia)
            $(this).val(min_gia)
            $('#range').val(min_gia)
            $(this).focus()
            return false
        }
    })

    //Them vao danh sach yeu thich
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item");
        let this_val = $(this);

        console.log("Id: "+ product_id);

        $.ajax({
            url: $(this).attr("action"), //add-to-wishlist/
            data: {
                "maSP": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.html('<i class="fa-solid fa-check"></i>')
            },
            success: function(reponse){
                if (reponse.bool == true){
                    console.log("Đã được thêm vào");
                }
            }
        })
    })

    //Xoa san pham trong danh sach yeu thich
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id is: ", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "maSP": wishlist_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Đang xóa sản phẩm");
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
            }
        })
    })

    //Xoa don hang trong danh sach dat hang
    $(document).on("click", ".remove-order", function(){
        let order_id = $(this).attr("order-id")
        let this_val = $(this)

        console.log("Order id: ", order_id)

        $.ajax({
            url: "/remove-orders",
            data: {
                "oid": order_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Đang xóa đơn hàng");
            },
            success: function(response){
                $("#HoaDon").html(response.data)
            }
        })
    })

    $(document).on("click", ".make-default-address", function(){
        let address_id = $(this).attr("data-address-id");
        let this_val = $(this)

        console.log(address_id);

        $.ajax({
            url: "/make-default-address",
            data: {
                "id": address_id,
            },
            dataType: "json",
            success: function(response){
                console.log("Da them dia chi thanh cong");
                if(response.boolean == true){
                    $(".check").hide();
                    $(".action_btn").show();

                    $(".check" + address_id).show();
                    $(".button" + address_id).hide();
                }
            }
        })
    })
})
