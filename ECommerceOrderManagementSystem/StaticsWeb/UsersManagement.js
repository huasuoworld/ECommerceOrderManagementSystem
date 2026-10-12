function userProfileValue(value) {
    return value === null || value === undefined || value === "" ? "—" : String(value);
}

const usersPageSize = 10;
let usersCurrentPage = 1;
let usersTotalPages = 0;

function loadUsers() {
    const $refreshButton = $("#refresh-users");
    $refreshButton.prop("disabled", true);
    $("#users-message").addClass("d-none").removeClass("alert-danger alert-warning").text("");
    $("#users-list").empty().append(
        $("<tr>").append($("<td>", {
            colspan: 6,
            class: "text-center text-secondary py-5"
        }).text("Loading users…"))
    );

    CommonUtil.request(
        `${CommonUtil.UsersManagementListUsersURL}?page_number=${usersCurrentPage}&page_size=${usersPageSize}`,
        CommonUtil.GET
    )
        .done((response) => {
            const users = Array.isArray(response.items) ? response.items : [];
            const totalUsers = Number(response.total_items) || 0;
            usersTotalPages = Number(response.total_pages) || 0;
            $("#users-count").text(`${totalUsers} ${totalUsers === 1 ? "user" : "users"}`);
            $("#users-list").empty();

            if (users.length === 0) {
                $("#users-list").append(
                    $("<tr>").append($("<td>", {
                        colspan: 6,
                        class: "text-center text-secondary py-5"
                    }).text("No users found."))
                );
                $("#users-pagination-summary").text("");
                $("#users-pagination").empty();
                return;
            }

            users.forEach((user) => {
                $("#users-list").append(
                    $("<tr>").append(
                        $("<td>").text(userProfileValue(user.username)),
                        $("<td>").text(userProfileValue(user.display_name)),
                        $("<td>").text(userProfileValue(user.user_email)),
                        $("<td>").text(userProfileValue(user.user_phone)),
                        $("<td>").append(
                            $("<span>", { class: "badge text-bg-secondary" })
                                .text(userProfileValue(user.user_status))
                        ),
                        $("<td>").text(userProfileValue(user.created_at))
                    )
                );
            });
            const start = (usersCurrentPage - 1) * usersPageSize + 1;
            const end = Math.min(start + users.length - 1, totalUsers);
            $("#users-pagination-summary").text(`Showing ${start}–${end} of ${totalUsers} users`);
            renderUsersPagination();
        })
        .fail((xhr) => {
            $("#users-count").text("");
            $("#users-list").empty().append(
                $("<tr>").append($("<td>", {
                    colspan: 6,
                    class: "text-center text-danger py-5"
                }).text("Unable to load users. Please try again."))
            );
            $("#users-pagination-summary").text("");
            $("#users-pagination").empty();
            $("#users-message")
                .removeClass("d-none")
                .addClass(xhr.status === 403 ? "alert-warning" : "alert-danger")
                .text(
                    xhr.status === 401
                        ? "Your session has expired. Please sign in again."
                        : xhr.status === 403
                        ? "Administrator permission is required to view the user list."
                        : xhr.responseJSON?.detail || "Please try again later."
                );
        })
        .always(() => $refreshButton.prop("disabled", false));
}

function renderUsersPagination() {
    const $pagination = $("#users-pagination").empty();
    if (usersTotalPages <= 1) {
        return;
    }

    $pagination.append(makeUsersPageButton("Previous", usersCurrentPage - 1, usersCurrentPage === 1));
    for (let page = 1; page <= usersTotalPages; page += 1) {
        $pagination.append(makeUsersPageButton(String(page), page, false, page === usersCurrentPage));
    }
    $pagination.append(
        makeUsersPageButton("Next", usersCurrentPage + 1, usersCurrentPage === usersTotalPages)
    );
}

function makeUsersPageButton(label, page, disabled, active = false) {
    const $button = $("<button>", {
        type: "button",
        class: "page-link",
        text: label
    }).attr("data-page", page);
    if (active) $button.attr("aria-current", "page");
    if (disabled) $button.prop("disabled", true);
    return $("<li>", {
        class: `page-item${active ? " active" : ""}${disabled ? " disabled" : ""}`
    }).append($button);
}

$(function () {
    loadUsers();
    $("#refresh-users").on("click", loadUsers);
    $("#users-pagination").on("click", "[data-page]", function () {
        const page = Number($(this).attr("data-page"));
        if (page >= 1 && page <= usersTotalPages && page !== usersCurrentPage) {
            usersCurrentPage = page;
            loadUsers();
        }
    });
});