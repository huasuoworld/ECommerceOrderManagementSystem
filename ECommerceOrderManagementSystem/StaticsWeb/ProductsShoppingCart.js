const formatCartPrice = (price) => `CA$${Number(price).toLocaleString("en-CA")}`;

function makeCartTextElement(tagName, className, text) {
    return $("<" + tagName + ">")
        .addClass(className)
        .text(text);
}

$(function () {
    loadCart();
});

function showCartMessage(message, type = "danger") {
    $("#cart-message")
        .removeClass("d-none alert-danger alert-success")
        .addClass(`alert-${type}`)
        .text(message);
}

function clearCartMessage() {
    $("#cart-message")
        .addClass("d-none")
        .removeClass("alert-danger alert-success")
        .empty();
}

function openCart() {
    $("#cart-panel").removeClass("d-none");
    $("#cart-toggle").attr("aria-expanded", "true");
}

function loadCart() {
    CommonUtil.request(CommonUtil.ShoppingCartURL, CommonUtil.GET)
        .done(renderCart)
        .fail((xhr) => showCartMessage(xhr.responseJSON?.detail || "Unable to load your cart."));
}

function renderCart(cart) {
    const cartItems = $("#cart-items").empty();
    const itemCount = cart.items.reduce((total, item) => total + item.products_quantity, 0);
    const subtotal = cart.items.reduce((total, item) => total + item.products_total_price, 0);
    $("#cart-item-count").text(itemCount);
    $("#cart-subtotal").text(formatCartPrice(subtotal));

    if (!cart.items.length) {
        cartItems.append(
            makeCartTextElement("p", "text-secondary mb-0", "Your cart is empty.")
        );
        return;
    }

    cart.items.forEach((item) => {
        const row = $("<div>", {
            class: "d-flex flex-column flex-sm-row align-items-sm-center justify-content-between gap-3 py-3 border-bottom"
        });
        const details = $("<div>", { class: "d-flex align-items-center gap-3" });
        if (item.product_img_url) {
            details.append($("<img>", {
                class: "cart-item-image",
                src: item.product_img_url,
                alt: item.product_name
            }));
        } else {
            details.append(makeCartTextElement("span", "cart-item-image", "◇"));
        }
        details.append(
            $("<div>").append(
                makeCartTextElement("h3", "h6 mb-1", item.product_name),
                makeCartTextElement("p", "small text-secondary mb-0", `${formatCartPrice(item.unit_price)} each`)
            )
        );

        const controls = $("<div>", { class: "d-flex align-items-center gap-2" });
        const decrease = $("<button>", {
            class: "btn btn-sm btn-outline-secondary",
            type: "button",
            text: "−",
            "aria-label": `Decrease quantity of ${item.product_name}`
        }).attr({
            "data-cart-quantity": item.product_id,
            "data-quantity": item.products_quantity - 1
        }).prop("disabled", item.products_quantity <= 1);
        const quantity = makeCartTextElement("span", "px-1", item.products_quantity);
        const increase = $("<button>", {
            class: "btn btn-sm btn-outline-secondary",
            type: "button",
            text: "+"
        }).attr({
            "data-cart-quantity": item.product_id,
            "data-quantity": item.products_quantity + 1,
            "aria-label": `Increase quantity of ${item.product_name}`
        });
        const remove = $("<button>", {
            class: "btn btn-sm btn-link text-danger",
            type: "button",
            text: "Remove",
            "aria-label": `Remove ${item.product_name} from cart`
        }).attr("data-remove-product", item.product_id);
        controls.append(decrease, quantity, increase, remove);
        row.append(details, controls);
        cartItems.append(row);
    });
}

function handleCartRequest(request) {
    clearCartMessage();
    request
        .done((cart) => {
            renderCart(cart);
            openCart();
        })
        .fail((xhr) => {
            showCartMessage(xhr.responseJSON?.detail || "Unable to update your cart.");
            openCart();
        });
}

$("#cart-toggle").on("click", function () {
    const isOpen = $(this).attr("aria-expanded") === "true";
    $("#cart-panel").toggleClass("d-none", isOpen);
    $(this).attr("aria-expanded", String(!isOpen));
});

$("#cart-close").on("click", function () {
    $("#cart-panel").addClass("d-none");
    $("#cart-toggle").attr("aria-expanded", "false").trigger("focus");
});

$(document).on("click", "[data-add-product]", function () {
    handleCartRequest(CommonUtil.request(CommonUtil.ShoppingCartItems, CommonUtil.POST, {
        product_id: Number($(this).attr("data-add-product")),
        quantity: 1
    }));
});

$(document).on("click", "[data-cart-quantity]", function () {
    handleCartRequest(CommonUtil.request(
        `${CommonUtil.ShoppingCartItems}/${Number($(this).attr("data-cart-quantity"))}`,
        CommonUtil.PATCH,
        { quantity: Number($(this).attr("data-quantity")) }
    ));
});

$(document).on("click", "[data-remove-product]", function () {
    handleCartRequest(CommonUtil.request(
        `${CommonUtil.ShoppingCartItems}/${Number($(this).attr("data-remove-product"))}`,
        CommonUtil.DELETE
    ));
});