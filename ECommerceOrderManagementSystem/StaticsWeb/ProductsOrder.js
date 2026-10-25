const orderFormatPrice = (price) => `CA$${Number(price || 0).toLocaleString("en-CA")}`;
let checkoutCart = null;
let checkoutConfirmed = false;
let checkoutOrderId = null;

function orderTextElement(tagName, className, text) {
    return $("<" + tagName + ">").addClass(className).text(text ?? "");
}

function showOrderMessage(message, type = "danger") {
    $("#order-message")
        .removeClass("d-none alert-danger alert-success alert-info")
        .addClass(`alert-${type}`)
        .text(message);
}

function loadOrders() {
    if (new URLSearchParams(window.location.search).get("checkout") === "1") {
        loadCheckout();
        return;
    }

    const orderList = $("#order-list").empty()
        .append(orderTextElement("p", "text-secondary", "Loading your orders..."));

    CommonUtil.request(CommonUtil.ProductsOrderURL, CommonUtil.GET)
        .done((response) => {
            if (!Array.isArray(response)) {
                showOrderMessage("The order service returned an invalid response.");
                orderList.empty();
                return;
            }

            renderOrders(response);
        })
        .fail((xhr) => {
            orderList.empty();
            showOrderMessage(
                xhr.responseJSON?.detail || xhr.responseJSON?.message || "Unable to load your orders."
            );
        });
}

function loadCheckout() {
    const orderList = $("#order-list").empty()
        .append(orderTextElement("p", "text-secondary", "Loading your cart..."));
    $("#checkout-confirmation").addClass("d-none").empty();
    checkoutConfirmed = false;
    checkoutOrderId = null;

    CommonUtil.request(CommonUtil.ShoppingCartURL, CommonUtil.GET)
        .done((response) => {
            if (!response || !Array.isArray(response.items)) {
                orderList.empty();
                showOrderMessage("The shopping cart service returned an invalid response.");
                return;
            }

            checkoutCart = response;
            if (checkoutCart.items.length === 0) {
                orderList.empty().append(
                    orderTextElement("p", "card card-body border-0 text-secondary mb-0", "Your checkout is empty. Return to the products page and add items first.")
                );
                return;
            }

            renderCheckout();
        })
        .fail((xhr) => {
            orderList.empty();
            showOrderMessage(
                xhr.responseJSON?.detail || xhr.responseJSON?.message || "Unable to load your cart for checkout."
            );
        });
}

function renderCheckout() {
    if (!checkoutCart) {
        return;
    }

    const orderList = $("#order-list").empty();
    $("#order-message").addClass("d-none").empty();
    $("#checkout-confirmation").addClass("d-none").empty();

    const subtotal = checkoutCart.items.reduce(
        (total, item) => total + Number(item.products_total_price || 0),
        0
    );
    const card = $("<article>", { class: "card order-card" });
    const cardBody = $("<div>", { class: "card-body p-4" });
    cardBody.append(
        orderTextElement("h2", "h5 order-number mb-3", "Review your order"),
        orderTextElement("p", "small text-secondary", "Confirming this order will submit it to the order service.")
    );

    checkoutCart.items.forEach((item) => {
        const line = $("<div>", {
            class: "d-flex justify-content-between gap-3 border-top py-3"
        }).append(
            orderTextElement("span", "", `${item.product_name} × ${item.products_quantity}`),
            orderTextElement(
                "span",
                "text-nowrap",
                orderFormatPrice(item.products_total_price)
            )
        );
        cardBody.append(line);
    });

    cardBody.append(
        $("<div>", {
            class: "d-flex justify-content-between border-top pt-3 fw-bold"
        }).append(
            orderTextElement("span", "", "Total"),
            orderTextElement("span", "order-total", orderFormatPrice(subtotal))
        )
    );

    if (checkoutConfirmed) {
        cardBody.append(
            orderTextElement("p", "alert alert-success mt-3 mb-0", "Your order has been confirmed.")
        );
        const confirmation = $("#checkout-confirmation").removeClass("d-none");
        if (checkoutOrderId !== null) {
            confirmation.append($("<button>", {
                class: "btn btn-success",
                type: "button",
                text: "Pay now"
            }).attr({
                "data-pay-order": checkoutOrderId,
                "data-checkout-pay": "true"
            }));
        } else {
            confirmation.append(
                orderTextElement("p", "text-secondary", "You can pay for this order from My Orders."),
                $("<a>", {
                    class: "btn btn-outline-success",
                    href: "/productsOrder",
                    text: "View My Orders"
                })
            );
        }
    } else {
        cardBody.append(
            $("<button>", {
                class: "btn btn-success mt-3",
                type: "button",
                text: "Confirm order"
            }).attr("data-confirm-checkout", "true")
        );
    }

    card.append(cardBody);
    orderList.append(card);
}

$(document).on("click", "[data-confirm-checkout]", function () {
    if (!checkoutCart || checkoutCart.items.length === 0) {
        showOrderMessage("Your cart is empty. Return to your cart and try again.");
        return;
    }

    const confirmButton = $(this).prop("disabled", true);
    CommonUtil.request(CommonUtil.ProductsOrderConfirmURL, CommonUtil.GET)
        .done((order) => {
            checkoutConfirmed = true;
            checkoutOrderId = order?.id ?? order?.products_order_id ?? null;
            renderCheckout();
            if (checkoutOrderId === null) {
                showOrderMessage("Your order was confirmed, but its ID was not returned. You can pay for it from My Orders.");
            }
        })
        .fail((xhr) => {
            confirmButton.prop("disabled", false);
            showOrderMessage(
                xhr.responseJSON?.detail || xhr.responseJSON?.message || "Unable to confirm your order."
            );
        });
});

function renderOrders(orders) {
    const orderList = $("#order-list").empty();
    $("#order-message").addClass("d-none").empty();

    if (!orders.length) {
        orderList.append(
            orderTextElement("p", "card card-body border-0 text-secondary mb-0", "You don't have any orders yet.")
        );
        return;
    }

    orders.forEach((order) => {
        const orderId = order.id ?? order.products_order_id;
        const orderNumber = order.order_number || `Order #${orderId}`;
        const paymentStatus = String(order.payment_status ?? "Unknown");
        const orderStatus = String(order.order_status ?? "Unknown");
        const card = $("<article>", { class: "card order-card" });
        const cardBody = $("<div>", { class: "card-body p-4" });
        const header = $("<div>", {
            class: "d-flex flex-column flex-sm-row align-items-sm-start justify-content-between gap-3"
        });
        const heading = $("<div>").append(
            orderTextElement("h2", "h5 order-number mb-1", orderNumber),
            orderTextElement(
                "p",
                "small text-secondary mb-0",
                order.created_at ? `Placed ${order.created_at}` : "Order date unavailable"
            )
        );
        const statusGroup = $("<div>", { class: "d-flex flex-wrap gap-2" }).append(
            $("<span>", { class: "badge text-bg-light border" }).text(`Order: ${orderStatus}`),
            $("<span>", { class: "badge text-bg-light border" }).text(`Payment: ${paymentStatus}`)
        );
        header.append(heading, statusGroup);

        const totals = $("<div>", {
            class: "d-flex flex-wrap align-items-end justify-content-between gap-3 border-top mt-3 pt-3"
        });
        const breakdown = $("<div>", { class: "small text-secondary" }).append(
            orderTextElement("div", "", `Products: ${orderFormatPrice(order.order_product_price)}`),
            orderTextElement("div", "", `Discount: −${orderFormatPrice(order.order_discount_price)}`),
            orderTextElement("div", "", `Freight: ${orderFormatPrice(order.order_freight_price)}`)
        );
        totals.append(
            breakdown,
            orderTextElement("div", "order-total fw-bold", orderFormatPrice(order.order_amount))
        );
        cardBody.append(header, totals);
        if (orderId !== undefined && orderId !== null && !isOrderPaid(paymentStatus)) {
            cardBody.append(
                $("<button>", {
                    class: "btn btn-success mt-3",
                    type: "button",
                    text: "Pay now"
                }).attr("data-pay-order", orderId)
            );
        }

        card.append(cardBody);
        orderList.append(card);
    });
}

function isOrderPaid(paymentStatus) {
    return ["Paying", "Paid"].includes(
        String(paymentStatus).trim().toLowerCase()
    );
}

$(function () {
    loadOrders();
});