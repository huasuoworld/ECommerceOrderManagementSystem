$(document).on("click", "[data-pay-order]", function () {
    const button = $(this);
    const orderId = button.attr("data-pay-order");
    if (!orderId) {
        showOrderMessage("Unable to start payment because the order ID is missing.");
        return;
    }

    button.prop("disabled", true).text("Processing payment...");
    CommonUtil.request(
        `${CommonUtil.ProductsOrderPaymentURL}?orderId=${encodeURIComponent(orderId)}`,
        CommonUtil.GET
    )
        .done(() => {
            button
                .removeAttr("data-pay-order")
                .prop("disabled", true)
                .text("Paid");

            if (button.is("[data-checkout-pay]")) {
                showOrderMessage("Payment completed successfully.", "success");
            } else {
                button.closest(".order-card").find(".badge").eq(1).text("Payment: Paid");
                showOrderMessage("Payment completed successfully.", "success");
            }
        })
        .fail((xhr) => {
            button.prop("disabled", false).text("Pay now");
            showOrderMessage(
                xhr.responseJSON?.detail || xhr.responseJSON?.message || "Unable to complete payment."
            );
        });
});