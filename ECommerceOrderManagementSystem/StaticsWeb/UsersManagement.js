function userProfileValue(value) {
    return value === null || value === undefined || value === "" ? "—" : String(value);
}

function loadUserProfile() {
    const $refreshButton = $("#refresh-profile");
    $refreshButton.prop("disabled", true);
    $("#profile-message").addClass("d-none").text("");
    $("#profile-details").empty().append(
        $("<tr>").append($("<td>", {
            colspan: 6,
            class: "text-center text-secondary py-5"
        }).text("Loading account profile…"))
    );

    CommonUtil.request("/users/me", CommonUtil.GET)
        .done((profile) => {
            $("#profile-summary").text("1 account");
            $("#profile-details").empty().append(
                $("<tr>").append(
                    $("<td>").text(userProfileValue(profile.username)),
                    $("<td>").text(userProfileValue(profile.display_name)),
                    $("<td>").text(userProfileValue(profile.user_email)),
                    $("<td>").text(userProfileValue(profile.user_phone)),
                    $("<td>").append(
                        $("<span>", { class: "badge text-bg-secondary" })
                            .text(userProfileValue(profile.user_status))
                    ),
                    $("<td>").text(userProfileValue(profile.created_at))
                )
            );
        })
        .fail((xhr) => {
            $("#profile-summary").text("");
            $("#profile-details").empty().append(
                $("<tr>").append($("<td>", {
                    colspan: 6,
                    class: "text-center text-danger py-5"
                }).text("Unable to load the account profile."))
            );
            $("#profile-message")
                .removeClass("d-none")
                .addClass("alert-danger")
                .text(
                    xhr.status === 401
                        ? "Your session has expired. Please sign in again."
                        : xhr.responseJSON?.detail || "Please try again later."
                );
        })
        .always(() => $refreshButton.prop("disabled", false));
}

$(function () {
    loadUserProfile();
    $("#refresh-profile").on("click", loadUserProfile);
});