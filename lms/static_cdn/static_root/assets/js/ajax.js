$(document).ready(function () {
        var lessonForm = $('.form-lesson-ajax')
        lessonForm.submit(function (event) {
            event.preventDefault();
            var thisForm = $(this)
            // var actionEndpoint = thisForm.attr("action");   // api endpoint
            var actionEndpoint = thisForm.attr("data-endpoint")
            var httpMethod = thisForm.attr("method");
            var formData = thisForm.serialize();

            $.ajax({
                url: actionEndpoint,
                method: httpMethod,
                data: formData,
                success: function (data) {
                    var submitSpan = thisForm.find(".submit-span")
                    if (data.added){
                        submitSpan.html(
                            '<button type="submit" style="background: #fff; border: none; margin: -10px;"><i class="material-icons notranslate color-red icon--left">remove_shopping_cart</i></button>'
                        )
                    } else {
                        submitSpan.html(
                            '<button type="submit" style="background: #fff; border: none; margin: -10px;"><i class="material-icons notranslate color-red icon--left">shopping_cart</i></button>'
                        )
                    }
                    var cartCount = $('.cart-count')
                    cartCount.text(data.cartItemCount)
                    var currentPath = window.location.href
                    if (currentPath.indexOf("cart") != -1){
                        refreshCart()
                    }
                },
                error(errorData){
                    console.log("error");
                    console.log(errorData);
                }
            })
        })
    })