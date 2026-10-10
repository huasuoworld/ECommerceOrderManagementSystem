(function(window) {
    // Constants for all js
    const Constants = Object.freeze({
        SuccessStatusCode: 200,
        ErrorStatusCode: 400,
        GET: "GET",
        POST: "POST",
        PATCH: "PATCH",
        DELETE: "DELETE",
        UserSessionID: "userSessionID",
        UserSessionIDCookiePath: "/",
        ShoppingCartURL: "/shoppingCart",
        ShoppingCartItems: "/shoppingCart/items",
        UsersLogin: "/users/login",
        USER_STATUS: {
            ACTIVE: 1,
            INACTIVE: 0
        }
    });
    // JQuery http functions
    const http = {
        request: function(httpUrl, method, formData) {
            const requestOptions = {
                url: httpUrl,
                method: method,
                dataType: "json"
            };
            const userSessionID = Cookies.get(Constants.UserSessionID);

            if (userSessionID) {
                requestOptions.headers = {
                    [Constants.UserSessionID]: userSessionID
                };
            }

            if (formData !== undefined) {
                requestOptions.contentType = "application/json";
                requestOptions.data = JSON.stringify(formData);
            }

            return $.ajax(requestOptions);
        }
    };

    const cookieStore = {
        set: function(key, value, days = 1) {
            Cookies.set(key, value, {expires: days, path: Constants.UserSessionIDCookiePath});
        },
        get: function(key) {
            return Cookies.get(key);
        },
        remove: function(key) {
            Cookies.remove(key, {path: Constants.UserSessionIDCookiePath})
        },
        getSessionId: function() {
            return Cookies.get(Constants.UserSessionID);
        }
    };

    // 挂载到全局
    window.CommonUtil = {
        ...Constants,
        ...http,
        ...cookieStore
    };

})(window);