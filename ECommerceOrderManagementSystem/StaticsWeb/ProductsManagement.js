const productsPageSize = 10;
let productsCurrentPage = 1;
let productsTotalPages = 0;

function productCellText(value, fallback = "—") {
    return value === null || value === undefined || value === "" ? fallback : String(value);
}

function renderProductRow(product) {
    const productCell = $("<div>", { class: "d-flex align-items-center gap-3" });
    if (product.product_img_url) {
        productCell.append($("<img>", {
            class: "rounded border",
            src: product.product_img_url,
            alt: "",
            width: 56,
            height: 56,
            loading: "lazy"
        }).css({ objectFit: "cover" }));
    }
    productCell.append($("<div>").append(
        $("<div>", { class: "fw-semibold" }).text(productCellText(product.product_name)),
        $("<div>", { class: "small text-secondary" }).text(productCellText(product.product_sub_name))
    ));

    const price = Number(product.product_price);
    const priceText = Number.isFinite(price)
        ? new Intl.NumberFormat("en-CA", { style: "currency", currency: "CAD" }).format(price)
        : "—";
    const inventory = productCellText(product.inventory_status, "Unknown");
    const inventoryClass = inventory === "In Stock"
        ? "text-bg-success"
        : inventory === "Out of Stock"
            ? "text-bg-danger"
            : "text-bg-secondary";

    return $("<tr>").append(
        $("<td>").append(productCell),
        $("<td>").text(
            `${productCellText(product.category_name)} / ${productCellText(product.brand_name)}`
        ),
        $("<td>").append($("<code>").text(productCellText(product.product_code))),
        $("<td>", { class: "text-end text-nowrap" }).text(priceText),
        $("<td>").append($("<span>", { class: `badge ${inventoryClass}` }).text(inventory))
    );
}

function showProductMessage(message, type) {
    $("#product-message")
        .removeClass("d-none alert-info alert-danger")
        .addClass(`alert-${type}`)
        .text(message);
}

function loadManagedProducts() {
    $("#refresh-products").prop("disabled", true);
    $("#product-message").addClass("d-none").text("");
    $("#product-list").empty().append(
        $("<tr>").append($("<td>", {
            colspan: 5,
            class: "text-center text-secondary py-5"
        }).text("Loading products…"))
    );

    CommonUtil.request(
        `/products/listProducts?page_number=${productsCurrentPage}&page_size=${productsPageSize}`,
        CommonUtil.GET
    )
        .done((response) => {
            const items = Array.isArray(response.items) ? response.items : [];
            const totalItems = Number(response.total_items) || 0;
            productsTotalPages = Number(response.total_pages) || 0;
            $("#product-count").text(`${totalItems} ${totalItems === 1 ? "product" : "products"}`);
            $("#product-list").empty();

            if (items.length === 0) {
                $("#product-list").append(
                    $("<tr>").append($("<td>", {
                        colspan: 5,
                        class: "text-center text-secondary py-5"
                    }).text("No products found."))
                );
                $("#pagination-summary").text("");
                $("#product-pagination").empty();
                return;
            }

            items.forEach((product) => $("#product-list").append(renderProductRow(product)));
            const start = (productsCurrentPage - 1) * productsPageSize + 1;
            const end = Math.min(start + items.length - 1, totalItems);
            $("#pagination-summary").text(`Showing ${start}–${end} of ${totalItems} products`);
            renderProductPagination();
        })
        .fail((xhr) => {
            $("#product-count").text("");
            $("#product-list").empty().append(
                $("<tr>").append($("<td>", {
                    colspan: 5,
                    class: "text-center text-danger py-5"
                }).text("Unable to load products. Please try again."))
            );
            $("#pagination-summary").text("");
            $("#product-pagination").empty();
            showProductMessage(
                xhr.responseJSON?.detail || xhr.responseJSON?.message || "Unable to load the product list.",
                "danger"
            );
        })
        .always(() => $("#refresh-products").prop("disabled", false));
}

function renderProductPagination() {
    const pagination = $("#product-pagination").empty();
    if (productsTotalPages <= 1) {
        return;
    }

    pagination.append(makeProductPageButton("Previous", productsCurrentPage - 1, productsCurrentPage === 1));
    for (let page = 1; page <= productsTotalPages; page += 1) {
        pagination.append(makeProductPageButton(String(page), page, false, page === productsCurrentPage));
    }
    pagination.append(makeProductPageButton("Next", productsCurrentPage + 1, productsCurrentPage === productsTotalPages));
}

function makeProductPageButton(label, page, disabled, active = false) {
    const button = $("<button>", {
        type: "button",
        class: "page-link",
        text: label
    }).attr("data-page", page);
    if (active) button.attr("aria-current", "page");
    if (disabled) button.prop("disabled", true);
    return $("<li>", { class: `page-item${active ? " active" : ""}${disabled ? " disabled" : ""}` })
        .append(button);
}

$(function () {
    loadManagedProducts();
    $("#refresh-products").on("click", loadManagedProducts);
    $("#product-pagination").on("click", "[data-page]", function () {
        const page = Number($(this).attr("data-page"));
        if (page >= 1 && page <= productsTotalPages && page !== productsCurrentPage) {
            productsCurrentPage = page;
            loadManagedProducts();
        }
    });
});