$(function () {
	const $form = $("#login-form");
	const $username = $("#username");
	const $password = $("#password");
	const $feedback = $("#login-feedback");
	const $submitButton = $("#submit-button");

	$("#toggle-password").on("click", function () {
		const isVisible = $password.attr("type") === "text";
		$password.attr("type", isVisible ? "password" : "text");
		$(this).attr("aria-pressed", String(!isVisible)).text(isVisible ? "Show" : "Hide");
	});

	$form.on("submit", function (event) {
		event.preventDefault();

		if (!this.reportValidity()) {
			return;
		}

		$submitButton.prop("disabled", true).text("Signing in...");
		$feedback.removeClass("alert-danger alert-success").addClass("alert-secondary").text("Checking your account...");

		const userModel = {
			username: $username.val().trim(),
			password: $password.val()
		};

		CommonUtil.request(CommonUtil.UsersLogin, CommonUtil.POST, userModel).done(function (response) {
			const isAuthenticated = Number(response.status) === CommonUtil.SuccessStatusCode;
			if (isAuthenticated && response.data) {
				CommonUtil.set(CommonUtil.UserSessionID, response.data);
			}
			$feedback
				.removeClass("alert-secondary alert-danger alert-success")
				.addClass(isAuthenticated ? "alert-success" : "alert-danger")
				.text(response.message || "Unable to sign in.");
		}).fail(function (xhr) {
			const message = xhr.responseJSON && xhr.responseJSON.detail
				? "Please check the information you entered."
				: "The service is unavailable. Please try again.";
			$feedback.removeClass("alert-secondary alert-success").addClass("alert-danger").text(message);
		}).always(function () {
			$submitButton.prop("disabled", false).text("Sign in");
		});
	});
});
