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
            colspan: 7,
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
                        colspan: 7,
                        class: "text-center text-secondary py-5"
                    }).text("No users found."))
                );
                $("#users-pagination-summary").text("");
                $("#users-pagination").empty();
                return;
            }

            users.forEach((user) => {
                const isActive = user.user_status === "active";
                const actionStatus = isActive ? "inactive" : "active";
                const actionLabel = isActive ? "Disable" : "Activate";
                const actionClass = isActive ? "btn-outline-danger" : "btn-outline-success";
                $("#users-list").append(
                    $("<tr>").append(
                        $("<td>").text(userProfileValue(user.username)),
                        $("<td>").text(userProfileValue(user.display_name)),
                        $("<td>").text(userProfileValue(user.user_email)),
                        $("<td>").text(userProfileValue(user.user_phone)),
                        $("<td>").append(
                            $("<span>", {
                                class: `badge ${isActive ? "text-bg-success" : "text-bg-secondary"}`
                            })
                                .text(userProfileValue(user.user_status))
                        ),
                        $("<td>").text(userProfileValue(user.created_at)),
                        $("<td>").append(
                            $("<button>", {
                                type: "button",
                                class: `btn btn-sm ${actionClass}`,
                                text: actionLabel
                            })
                                .attr("data-user-id", user.id)
                                .attr("data-user-status", actionStatus)
                        )
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
                    colspan: 7,
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

function updateUserStatus(userId, userStatus, $button) {
    const url = userStatus === "active"
        ? CommonUtil.UsersManagementActiveUserURL
        : CommonUtil.UsersManagementInactiveUserURL;
    const actionLabel = userStatus === "active" ? "activate" : "disable";
    $button.prop("disabled", true);
    $("#users-message").addClass("d-none").removeClass("alert-danger alert-warning").text("");

    CommonUtil.request(`${url}?userId=${encodeURIComponent(userId)}`, CommonUtil.PATCH)
        .done((response) => {
            if (response.status !== CommonUtil.SuccessStatusCode) {
                $button.prop("disabled", false);
                $("#users-message")
                    .removeClass("d-none")
                    .addClass("alert-danger")
                    .text(response.message || `Unable to ${actionLabel} this user.`);
                return;
            }
            loadUsers();
        })
        .fail((xhr) => {
            $button.prop("disabled", false);
            $("#users-message")
                .removeClass("d-none")
                .addClass(xhr.status === 403 ? "alert-warning" : "alert-danger")
                .text(
                    xhr.status === 401
                        ? "Your session has expired. Please sign in again."
                        : xhr.status === 403
                        ? "Administrator permission is required to update user status."
                        : xhr.responseJSON?.detail || `Unable to ${actionLabel} this user. Please try again.`
                );
        });
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


// Notification pagination state
let currentMsgPage = 1;
let msgPageSize = 5; // Number of notifications per page
let totalMsgPages = 1;

/**
 * Initialize the notification system.
 */
function initNotificationSystem() {
    // Load the first page when the dropdown opens.
    const dropdownEl = document.getElementById('messagesDropdown');
    if (dropdownEl) {
        dropdownEl.addEventListener('show.bs.dropdown', function () {
            loadNotificationMessages(1);
        });
    }

    // Bind pagination controls.
    document.getElementById('prevMsgPage')?.addEventListener('click', function (e) {
        e.stopPropagation(); // Keep the dropdown open.
        if (currentMsgPage > 1) {
            loadNotificationMessages(currentMsgPage - 1);
        }
    });

    document.getElementById('nextMsgPage')?.addEventListener('click', function (e) {
        e.stopPropagation(); // Keep the dropdown open.
        if (currentMsgPage < totalMsgPages) {
            loadNotificationMessages(currentMsgPage + 1);
        }
    });
}

/**
 * Fetch and render a page of notifications.
 * @param {number} pageNumber
 */
function loadNotificationMessages(pageNumber) {
    const url = `/notification/getMessages?page_number=${pageNumber}&page_size=${msgPageSize}`;
    const container = document.getElementById('notificationListContainer');
    if (container) {
        container.innerHTML = '<li><span class="dropdown-item text-muted text-center py-2">Loading notifications...</span></li>';
    }

    CommonUtil.request(url, CommonUtil.POST)
    .done((res) => {
        if (res.status === CommonUtil.SuccessStatusCode && Array.isArray(res.items)) {
            currentMsgPage = Number(res.page_number) || pageNumber;
            totalMsgPages = Number(res.total_pages) || 0;
            renderNotificationList(res.items);
            updateMsgPaginationUI(currentMsgPage);
        } else {
            console.error("Failed to load notifications:", res.message);
            renderNotificationError(res.message || "Unable to load notifications.");
        }
    }).fail((xhr) => {
        const message = xhr.responseJSON?.message || "Unable to load notifications. Please try again later.";
        console.error("Failed to load notifications:", message);
        renderNotificationError(message);
    });
}

function renderNotificationError(message) {
    const container = document.getElementById('notificationListContainer');
    if (!container) return;

    const item = document.createElement('li');
    const text = document.createElement('span');
    text.className = 'dropdown-item text-danger text-center py-2';
    text.textContent = message;
    item.appendChild(text);
    container.replaceChildren(item);
}

/**
 * Render the notification dropdown list.
 * NotificationMessagesModel fields: message_code, message, message_type, message_status
 */
function renderNotificationList(list) {
    const container = document.getElementById('notificationListContainer');
    if (!container) return;

    if (!list || list.length === 0) {
        container.innerHTML = '<li><span class="dropdown-item text-muted text-center py-2">No notifications</span></li>';
        return;
    }

    const fragment = document.createDocumentFragment();
    list.forEach(item => {
        const unreadClass = item.message_status ? '' : 'bg-light fw-bold';
        const listItem = document.createElement('li');
        const messageItem = document.createElement('div');
        messageItem.className = `dropdown-item-text py-2 border-bottom ${unreadClass}`;

        const badges = document.createElement('div');
        badges.className = 'd-flex justify-content-between align-items-center mb-1';
        const typeBadge = document.createElement('span');
        typeBadge.className = 'badge bg-info text-dark';
        typeBadge.textContent = item.message_type || 'Notification';
        const statusBadge = document.createElement('span');
        statusBadge.className = `badge ${item.message_status ? 'bg-secondary' : 'bg-primary'}`;
        statusBadge.textContent = item.message_status ? 'Read' : 'Unread';
        badges.append(typeBadge, statusBadge);

        const messageText = document.createElement('p');
        messageText.className = 'mb-0 text-truncate';
        messageText.style.maxWidth = '280px';
        messageText.title = item.message || '';
        messageText.textContent = item.message || '';
        messageItem.append(badges, messageText);
        listItem.appendChild(messageItem);
        fragment.appendChild(listItem);
    });
    container.replaceChildren(fragment);
}

/**
 * Update the pagination controls.
 */
function updateMsgPaginationUI(pageNumber) {
    document.getElementById('msgPageInfo').innerText = `Page ${pageNumber} of ${totalMsgPages || 1}`;
    
    const prevBtn = document.getElementById('prevMsgPage');
    const nextBtn = document.getElementById('nextMsgPage');

    if (prevBtn) prevBtn.disabled = (pageNumber <= 1);
    
    if (nextBtn) nextBtn.disabled = pageNumber >= totalMsgPages;
}

$(function () {
    loadUsers();
    initNotificationSystem();
    $("#refresh-users").on("click", loadUsers);
    $("#users-list").on("click", "[data-user-status]", function () {
        updateUserStatus(
            $(this).attr("data-user-id"),
            $(this).attr("data-user-status"),
            $(this)
        );
    });
    $("#users-pagination").on("click", "[data-page]", function () {
        const page = Number($(this).attr("data-page"));
        if (page >= 1 && page <= usersTotalPages && page !== usersCurrentPage) {
            usersCurrentPage = page;
            loadUsers();
        }
    });
});
