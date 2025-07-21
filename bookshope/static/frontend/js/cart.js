
$(document).ready(function () {
    
    // document.querySelectorAll('.product-qty-box').forEach(box => {
    document.querySelectorAll('.quantity-selector, .pocket-product-qty').forEach(box => {
        const incrementBtn = box.querySelector('.increment');
        const decrementBtn = box.querySelector('.decrement');
        const qtyInput = box.querySelector('.cart_qty');

        const originalPriceElement = document.getElementById("originalPrice");
        const discountElement = document.getElementById("discountPercent");
        const currentPriceElement = document.getElementById("currentPrice");
        const basePrice = parseFloat(originalPriceElement.dataset.price);
        const discountPercent = parseFloat(discountElement.dataset.discount);

        function updateCurrentPrice() {
        const quantity = parseInt(qtyInput.value);
        const totalOriginalPrice = basePrice * quantity;
        const discountAmount = (discountPercent / 100) * totalOriginalPrice;
        const finalPrice = totalOriginalPrice - discountAmount;

            currentPriceElement.textContent = "৳" + finalPrice.toFixed(2);
        }

        incrementBtn.addEventListener('click', () => {
            let currentValue = parseInt(qtyInput.value) || 0;
            const maxValue = parseInt(qtyInput.max) || 50;
            if (currentValue < maxValue) {
                qtyInput.value = currentValue + 1;
                updateCart(qtyInput);
                updateCurrentPrice();
                
            }
        });
    

        decrementBtn.addEventListener('click', () => {
            let currentValue = parseInt(qtyInput.value) || 0;
            const minValue = parseInt(qtyInput.min) || 0;
            if (currentValue > minValue) {
                qtyInput.value = currentValue - 1;
                updateCart(qtyInput);
                updateCurrentPrice();
            }
        });
    

        qtyInput.addEventListener("input", function () {
            let val = parseInt(quantityInput.value);
            if (isNaN(val) || val < 1) val = 1;
            if (val > 10) val = 10;
                quantityInput.value = val;
                updateCurrentPrice();
        
        });

        // Initial calculation on page load
        updateCurrentPrice();
    });

   
    $('#add_to_cart').on('click', function (e) {
        console.log('in on click cart',e)
        e.preventDefault();
        const parentRow = $(this).parent().parent();
        
        if (parentRow.length) {
            // const qtyInput = document.getElementById('cart_qty');
            const qtyInput = parentRow.find('#cart_qty');

            if (qtyInput.length) {
                let currentValue = parseInt(qtyInput.val()) || 0;
                if (currentValue === 0) {
                    // qtyInput.value = 1;
                    qtyInput.val(1);
                } else {
                    // qtyInput.value = 0;
                    qtyInput.val(0);
                }        
                updateCart(qtyInput);
            }
        }
    });

    // document.querySelectorAll('button[id^="delete_cart__"]').forEach(deleteLink => {
    //     deleteLink.onclick = function (event) {
    //         event.preventDefault();
    //         const parentRow = this.closest('tr');
    //         // console.log(parentRow);

    //         if (parentRow) {
    //             console.log('Parent Row:', parentRow);
    //             parentRow.remove();

    //             const qtyInput = parentRow.querySelector('#cart_qty');

    //             let currentValue = parseInt(qtyInput.value) || 0;
    //             if (currentValue === 0) {
    //                 qtyInput.value = 1;
    //             } else {
    //                 qtyInput.value = 0;
    //             }        
    //             updateCart(qtyInput);
    //         }
    //     };
    // });
        const cartItemsContainer = document.querySelector('.cart-items');
        const cartItemElements = document.querySelectorAll('.cart-item');
        const emptyCartMessage = document.getElementById('emptyCartMessage');
        const cartSummary = document.querySelector('.cart-summary');

        if (cartItemElements.length === 0) {
            
            emptyCartMessage.style.display = 'block';  // show message
            cartSummary.style.display = 'none';        // hide summary
        } else {
            emptyCartMessage.style.display = 'none';   // hide message
            cartSummary.style.display = 'block';       // show summary
        }

    document.querySelectorAll('button[id^="delete_cart__"]').forEach(deleteBtn => {
        deleteBtn.onclick = function (event) {
            event.preventDefault();
            const productId = this.id.replace("delete_cart__", "");
            const cartItem = document.querySelector(".cart_item__" + productId);
            const qtyInput = cartItem.querySelector(".cart_qty");

            if (qtyInput) {
                qtyInput.value = 0;
                updateCart(qtyInput);
            }

            if (cartItem) {
                cartItem.remove(); // Remove item visually
            }
        };
    });

    
    function updateCart(qtyInput) {
        const productId = $(qtyInput).data('product-id');
        const newQty = $(qtyInput).val();
        
        $.ajax({
            url: '/add-or-update-cart/',
            type: 'POST',
            data: {
                'product_id': productId,
                'quantity': newQty,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function (response) {
                console.log(response);


                if (!response.is_authenticated) {
                    console.log('not auth')
                    const currentUrl = window.location.href;
                    const loginUrl = `/login/?next=${encodeURIComponent(currentUrl)}`;
                    
                    window.location.href = loginUrl;
                    return;
                } else if (response.status === 'success') {
                    // Update Cart Quantity
                    var itemQuantityElements = document.getElementsByClassName('cart_qty__' + productId);
                    Array.from(itemQuantityElements).forEach(function (itemQuantityElement) {
                        itemQuantityElement.value = newQty;
                    });
                    // Update Cart Quantity
                    
                    // Update Cart Item
                    if (response.isRemoved) {
                        var cartItemElements = document.getElementsByClassName('cart_item__' + productId);
                        Array.from(cartItemElements).forEach(function (cartItemElement) {
                            cartItemElement.remove();
                        });
                    } else {
                        var itemPriceElements = document.getElementsByClassName('total_price__' + productId);
                        Array.from(itemPriceElements).forEach(function (itemPriceElement) {
                            itemPriceElement.innerHTML = `${response.item_price.toFixed(2)}`;
                        });
                    }
                    // Update Cart Item

                    var addButton = document.getElementById('add_to_cart');
                    if (addButton) {
                        if (newQty == 1 && addButton.innerHTML == 'Add to Cart') { location.reload(); }
                        
                        if (newQty > 0) { addButton.innerHTML = 'Remove from Cart'; }
                        else { addButton.innerHTML = 'Add to Cart'; }
                    }

                    // Update Cart Amounts
                    var subTotalAmountElements = document.getElementsByClassName('sub_total_amount');
                    Array.from(subTotalAmountElements).forEach(function (subTotalAmountElement) {
                        subTotalAmountElement.innerHTML = `${response.amount_summary.sub_total_amount.toFixed(2)}`;
                    });
                    // var subTotalAmount = document.getElementById('sub_total_amount');
                    // if (subTotalAmount) { subTotalAmount.innerHTML = `${response.amount_summary.sub_total_amount.toFixed(2)}`; }
                    
                    var vatAmount = document.getElementById('total_vat');
                    if (vatAmount) { vatAmount.innerHTML = `${response.amount_summary.total_vat.toFixed(2)}`; }
                    
                    var discountAmount = document.getElementById('total_discount');
                    if (discountAmount) { discountAmount.innerHTML = `${response.amount_summary.total_discount.toFixed(2)}`; }
                    
                    var grandTotalAmount = document.getElementById('grand_total');
                    if (grandTotalAmount) { grandTotalAmount.innerHTML = `${response.amount_summary.grand_total.toFixed(2)}`; }

                    
                    var cartItemCountElements = document.getElementsByClassName('cart_item_quantity');
                    Array.from(cartItemCountElements).forEach(function (cartItemCountElement) {
                        cartItemCountElement.innerHTML = response.cart_item_count;
                    });
                    // var cartItemCount = document.getElementById('cart_item_quantity');
                    // if (cartItemCount) {
                    //     if (response.cart_item_count > 0) {
                    //         cartItemCount.innerHTML = response.cart_item_count;
                    //         cartItemCount.style.display = 'inline-block';
                    //     } else {
                    //         cartItemCount.style.display = 'none';
                    //     }
                    // }
                    // Update Cart Amounts
                } else {
                    alert('Failed to update the cart: ' + response.message);
                }
            },
            error: function (response) {
                console.error('Error updating cart:', response);
                if (!response.is_authenticated) {
                    console.log('in error not auth', response)
                    const currentUrl = window.location.pathname;
                    const loginUrl = `/login/?next=${encodeURIComponent(currentUrl)}`;
                    
                    window.location.href = loginUrl;
                    return;
                } else {
                    alert('An error occurred while updating the cart.');
                }
            }
        });
    }

    $('.cart_qty').on('change', function () {
        const productId = $(this).data('product-id');
        const newQty = $(this).val();
        updateCart(this);
    });
    
});



document.addEventListener('DOMContentLoaded', function () {
    const cartItemsContainer = document.querySelector('.cart-items');
    const emptyCartMessage = document.getElementById('emptyCartMessage');
    const cartSummary = document.querySelector('.cart-summary');

    function checkCartIsEmpty() {
        const cartItemElements = cartItemsContainer.querySelectorAll('.cart-item');
        if (cartItemElements.length === 0) {
            emptyCartMessage.style.display = 'block';  
            cartSummary.style.display = 'none';        
        } else {
            emptyCartMessage.style.display = 'none';   
            cartSummary.style.display = 'block';      
        }
    }

    checkCartIsEmpty();

    const observer = new MutationObserver(checkCartIsEmpty);
    observer.observe(cartItemsContainer, { childList: true, subtree: false });
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-btn')) {
            const productId = e.target.id.split('__')[1];
            const cartItem = document.querySelector(`.cart_item__${productId}`);
            if (cartItem) {
                cartItem.remove();  
                checkCartIsEmpty(); 
            }
        }
    });
});


// document.addEventListener('DOMContentLoaded', function () {
//         const cartToggleBtn = document.getElementById('cartToggleBtn');
//         const pocketBox = document.getElementById('cart-pocket-box');
//         const currencyBox = document.getElementById('currency-box'); // if exists

//         if (cartToggleBtn) {
//             cartToggleBtn.addEventListener('click', function () {
//                 if (currencyBox) currencyBox.style.display = 'none';

//                 if (pocketBox.style.display === 'block') {
//                     pocketBox.style.display = 'none';
//                     document.body.classList.remove('item-modal-open');
//                 } else {
//                     pocketBox.style.display = 'block';
//                     document.body.classList.add('item-modal-open');
//                 }
//             });
//         }
//     });


// document.addEventListener('DOMContentLoaded', function () {
//     const cartToggleBtn = document.getElementById('cartToggleBtn');
//     const cartBox = document.getElementById('cart-pocket-box');

//     // Toggle cart pocket visibility
//     cartToggleBtn.addEventListener('click', () => {
//         const isVisible = cartBox.style.display === 'block';
//         cartBox.style.display = isVisible ? 'none' : 'block';
//         document.body.classList.toggle('item-modal-open', !isVisible);
//     });

//     // Increment/Decrement quantity buttons
//     document.querySelectorAll('.qty-btn').forEach(button => {
//         button.addEventListener('click', function () {
//             const productId = this.getAttribute('data-product-id');
//             const input = document.querySelector(`.qty-input[data-product-id="${productId}"]`);
//             let value = parseInt(input.value) || 0;

//             if (this.classList.contains('increment')) {
//                 if (value < 50) value++;
//             } else if (this.classList.contains('decrement')) {
//                 if (value > 0) value--;
//             }

//             input.value = value;
//             updateCartTotal(productId, value);
//         });
//     });

//     // Update total price when input changes
//     document.querySelectorAll('.qty-input').forEach(input => {
//         input.addEventListener('input', function () {
//             const productId = this.getAttribute('data-product-id');
//             const value = parseInt(this.value) || 0;
//             updateCartTotal(productId, value);
//         });
//     });

//     function updateCartTotal(productId, quantity) {
//         // You would send AJAX to backend here to update the cart
//         // Example price (you can store original price in a hidden span or dataset)
//         const priceElement = document.querySelector(`.total_price__${productId}`);
//         const originalPrice = parseFloat(priceElement.dataset.unitPrice); // Add this via Django template
//         const newTotal = (originalPrice * quantity).toFixed(2);
//         priceElement.textContent = newTotal;

//         // Optional: update global cart total, count, etc.
//     }
// });

