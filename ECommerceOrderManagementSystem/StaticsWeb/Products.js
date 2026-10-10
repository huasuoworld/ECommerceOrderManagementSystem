const products = [
    {
        id: 1,
        category_name: "Apparel",
        category_code: "APPAREL",
        brand_name: "North Pine",
        brand_code: "NP",
        product_name: "City Lightweight Jacket",
        product_code: "NP-JK-001",
        product_price: 699,
        product_size: "S / M / L",
        product_color: "Pine Green",
        product_sub_name: "Lightweight protection for everyday commutes",
        product_description: "A clean silhouette and lightweight fabric provide comfortable protection for changing weather and city adventures.",
        product_img_url: "",
        product_status: "In stock",
        product_discount: 100,
        created_at: "2026-01-10",
        updated_at: "2026-06-18"
    },
    {
        id: 2,
        category_name: "Electronics",
        category_code: "DIGITAL",
        brand_name: "Sound Grove",
        brand_code: "SG",
        product_name: "Wireless Travel Earbuds",
        product_code: "SG-AU-204",
        product_price: 459,
        product_size: "One size",
        product_color: "Mist White",
        product_sub_name: "Clear sound, wherever you go",
        product_description: "Lightweight, comfortable earbuds for your commute, workouts, and everyday listening.",
        product_img_url: "",
        product_status: "In stock",
        product_discount: 0,
        created_at: "2026-02-03",
        updated_at: "2026-06-20"
    },
    {
        id: 3,
        category_name: "Lifestyle",
        category_code: "LIFESTYLE",
        brand_name: "Field Notes",
        brand_code: "FN",
        product_name: "Everyday Ceramic Mug",
        product_code: "FN-HM-032",
        product_price: 168,
        product_size: "350 ml",
        product_color: "Warm Sand",
        product_sub_name: "Make a moment for yourself",
        product_description: "A smooth glazed finish and just-right capacity make every drink feel like a little ritual.",
        product_img_url: "",
        product_status: "Low stock",
        product_discount: 20,
        created_at: "2026-03-12",
        updated_at: "2026-06-22"
    }
];

const formatPrice = (price) => `CA$${Number(price).toLocaleString("en-CA")}`;
const pageSize = 2;
let currentPage = 1;

function makeTextElement(tagName, className, text) {
    return $("<" + tagName + ">")
        .addClass(className)
        .text(text);
}

function renderProduct(product) {
    const card = $("<article>", { class: "card product-card h-100 rounded-2" });
    const imageArea = $("<div>", { class: "position-relative" });
    const status = $("<span>", {
        class: "badge rounded-pill text-bg-light position-absolute top-0 end-0 m-3"
    })
        .attr("aria-label", `Product status: ${product.product_status}`)
        .text(product.product_status);

    if (product.product_img_url) {
        imageArea.append(
            $("<img>", {
                class: "card-img-top product-image",
                src: product.product_img_url,
                alt: product.product_name
            })
        );
    } else {
        imageArea.append(makeTextElement("div", "image-placeholder", "◇"));
    }
    imageArea.append(status);

    const content = $("<div>", { class: "card-body d-flex flex-column p-4" });
    const meta = $("<div>", {
        class: "d-flex align-items-center justify-content-between gap-2 text-secondary small mb-2"
    }).append(
        makeTextElement("span", "fw-bold", product.category_name),
        makeTextElement("span", "", product.brand_name)
    );

    const name = makeTextElement("h2", "card-title product-name fw-bold mb-1", product.product_name);
    const subName = makeTextElement("p", "product-sub-name mb-0", product.product_sub_name);
    const description = makeTextElement("p", "product-description my-3", product.product_description);
    const attributes = $("<div>", { class: "d-flex flex-wrap gap-2 mb-3" }).append(
        makeTextElement("span", "badge attribute rounded-1 fw-normal", `Color: ${product.product_color}`),
        makeTextElement("span", "badge attribute rounded-1 fw-normal", `Size: ${product.product_size}`)
    );

    const footer = $("<div>", {
        class: "d-flex align-items-end justify-content-between gap-2 border-top pt-3 mt-auto"
    });
    const priceArea = $("<div>", { class: "d-flex flex-wrap align-items-baseline gap-2" });
    const discount = Number(product.product_discount) || 0;
    const hasDiscount = discount > 0;
    const currentPrice = hasDiscount
        ? Math.max(0, Number(product.product_price) - discount)
        : Number(product.product_price);

    priceArea.append(makeTextElement("span", "current-price", formatPrice(currentPrice)));
    if (hasDiscount) {
        priceArea.append(
            $("<del>", { class: "original-price" })
                .attr("aria-label", `Original price: ${formatPrice(product.product_price)}`)
                .text(formatPrice(product.product_price)),
            makeTextElement("span", "discount-label", `Save ${formatPrice(discount)}`)
        );
    }

    footer.append(
        priceArea,
        makeTextElement("span", "product-code text-end", `SKU ${product.product_code}`)
    );
    const addButton = $("<button>", {
        class: "btn btn-outline-success mt-3",
        type: "button",
        text: "Add to cart"
    }).attr("data-add-product", product.id);
    content.append(meta, name, subName, description, attributes, footer, addButton);
    card.append(imageArea, content);
    return $("<div>", { class: "col" }).append(card);
}

$(function () {
    $("#product-count").text(`${products.length} ${products.length === 1 ? "product" : "products"}`);
    loadCart();

    if (products.length) {
        renderProducts();
    } else {
        $("#product-list").append(
            $("<div>", { class: "col" }).append(
                makeTextElement("p", "alert alert-light text-center mb-0", "No products are available right now.")
            )
        );
        $("#pagination-summary, #product-pagination").hide();
    }
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
    $("#cart-item-count").text(cart.item_count);
    $("#cart-subtotal").text(formatPrice(cart.subtotal));

    if (!cart.items.length) {
        cartItems.append(
            makeTextElement("p", "text-secondary mb-0", "Your cart is empty.")
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
            details.append(makeTextElement("span", "cart-item-image", "◇"));
        }
        details.append(
            $("<div>").append(
                makeTextElement("h3", "h6 mb-1", item.product_name),
                makeTextElement("p", "small text-secondary mb-0", `${formatPrice(item.unit_price)} each`)
            )
        );

        const controls = $("<div>", { class: "d-flex align-items-center gap-2" });
        const decrease = $("<button>", {
            class: "btn btn-sm btn-outline-secondary",
            type: "button",
            text: "−",
            "aria-label": `Decrease quantity of ${item.product_name}`
        }).attr({
            "data-cart-quantity": item.id,
            "data-quantity": item.quantity - 1
        }).prop("disabled", item.quantity <= 1);
        const quantity = makeTextElement("span", "px-1", item.quantity);
        const increase = $("<button>", {
            class: "btn btn-sm btn-outline-secondary",
            type: "button",
            text: "+"
        }).attr({
            "data-cart-quantity": item.id,
            "data-quantity": item.quantity + 1,
            "aria-label": `Increase quantity of ${item.product_name}`
        });
        const remove = $("<button>", {
            class: "btn btn-sm btn-link text-danger",
            type: "button",
            text: "Remove",
            "aria-label": `Remove ${item.product_name} from cart`
        }).attr("data-remove-product", item.id);
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

function renderProducts() {
    const startIndex = (currentPage - 1) * pageSize;
    const pageProducts = products.slice(startIndex, startIndex + pageSize);
    const totalPages = Math.ceil(products.length / pageSize);
    const endIndex = Math.min(startIndex + pageProducts.length, products.length);

    $("#product-list").empty().append(pageProducts.map(renderProduct));
    $("#pagination-summary").text(
        `Showing ${startIndex + 1}–${endIndex} of ${products.length} products`
    );
    renderPagination(totalPages);
}

function renderPagination(totalPages) {
    const pagination = $("#product-pagination").empty();
    pagination.toggleClass("d-none", totalPages <= 1);

    if (totalPages <= 1) {
        return;
    }

    pagination.append(makePaginationItem("Previous", currentPage - 1, currentPage === 1));
    for (let page = 1; page <= totalPages; page += 1) {
        pagination.append(makePaginationItem(String(page), page, false, page === currentPage));
    }
    pagination.append(makePaginationItem("Next", currentPage + 1, currentPage === totalPages));
}

function makePaginationItem(label, page, disabled, active = false) {
    const button = $("<button>", {
        class: `page-link${active ? " active" : ""}`,
        type: "button",
        text: label
    }).attr("data-page", page);

    if (active) {
        button.attr("aria-current", "page").attr("aria-label", `Page ${page}`);
    }
    if (disabled) {
        button.prop("disabled", true);
    }

    return $("<li>", {
        class: `page-item${disabled ? " disabled" : ""}${active ? " active" : ""}`
    }).append(button);
}

$(document).on("click", "#product-pagination [data-page]", function () {
    const selectedPage = Number($(this).attr("data-page"));
    const totalPages = Math.ceil(products.length / pageSize);

    if (selectedPage >= 1 && selectedPage <= totalPages && selectedPage !== currentPage) {
        currentPage = selectedPage;
        renderProducts();
    }
});
