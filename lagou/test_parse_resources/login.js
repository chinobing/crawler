/*!dep/js-md5/src/md5.js*/
!function (a) {
    "use strict";
    var c = "undefined" != typeof module;
    c && (a = global, a.JS_MD5_TEST && (a.navigator = {userAgent: "Firefox"}));
    var h, A = (a.JS_MD5_TEST || !c) && -1 != navigator.userAgent.indexOf("Firefox"),
        g = !a.JS_MD5_TEST && "undefined" != typeof ArrayBuffer, y = "0123456789abcdef".split(""),
        v = [128, 32768, 8388608, -2147483648], S = [0, 8, 16, 24], T = [];
    if (g) {
        var _ = new ArrayBuffer(68);
        h = new Uint8Array(_), T = new Uint32Array(_)
    }
    var w = function (a) {
        var c = "string" != typeof a;
        c && a.constructor == ArrayBuffer && (a = new Uint8Array(a));
        var _, w, B, C, D, E, J, d, M, U, b, i, F = !0, H = !1, O = 0, j = 0, k = 0, z = a.length;
        T[16] = 0;
        do {
            if (T[0] = T[16], T[16] = T[1] = T[2] = T[3] = T[4] = T[5] = T[6] = T[7] = T[8] = T[9] = T[10] = T[11] = T[12] = T[13] = T[14] = T[15] = 0, c)if (g)for (i = j; z > O && 64 > i; ++O)h[i++] = a[O]; else for (i = j; z > O && 64 > i; ++O)T[i >> 2] |= a[O] << S[3 & i++]; else if (g)for (i = j; z > O && 64 > i; ++O)b = a.charCodeAt(O), 128 > b ? h[i++] = b : 2048 > b ? (h[i++] = 192 | b >> 6, h[i++] = 128 | 63 & b) : 55296 > b || b >= 57344 ? (h[i++] = 224 | b >> 12, h[i++] = 128 | b >> 6 & 63, h[i++] = 128 | 63 & b) : (b = 65536 + ((1023 & b) << 10 | 1023 & a.charCodeAt(++O)), h[i++] = 240 | b >> 18, h[i++] = 128 | b >> 12 & 63, h[i++] = 128 | b >> 6 & 63, h[i++] = 128 | 63 & b); else for (i = j; z > O && 64 > i; ++O)b = a.charCodeAt(O), 128 > b ? T[i >> 2] |= b << S[3 & i++] : 2048 > b ? (T[i >> 2] |= (192 | b >> 6) << S[3 & i++], T[i >> 2] |= (128 | 63 & b) << S[3 & i++]) : 55296 > b || b >= 57344 ? (T[i >> 2] |= (224 | b >> 12) << S[3 & i++], T[i >> 2] |= (128 | b >> 6 & 63) << S[3 & i++], T[i >> 2] |= (128 | 63 & b) << S[3 & i++]) : (b = 65536 + ((1023 & b) << 10 | 1023 & a.charCodeAt(++O)), T[i >> 2] |= (240 | b >> 18) << S[3 & i++], T[i >> 2] |= (128 | b >> 12 & 63) << S[3 & i++], T[i >> 2] |= (128 | b >> 6 & 63) << S[3 & i++], T[i >> 2] |= (128 | 63 & b) << S[3 & i++]);
            k += i - j, j = i - 64, O == z && (T[i >> 2] |= v[3 & i], ++O), O > z && 56 > i && (T[14] = k << 3, H = !0), F ? (D = T[0] - 680876937, D = (D << 7 | D >>> 25) - 271733879 << 0, d = (-1732584194 ^ 2004318071 & D) + T[1] - 117830708, d = (d << 12 | d >>> 20) + D << 0, J = (-271733879 ^ d & (-271733879 ^ D)) + T[2] - 1126478375, J = (J << 17 | J >>> 15) + d << 0, E = (D ^ J & (d ^ D)) + T[3] - 1316259209, E = (E << 22 | E >>> 10) + J << 0) : (D = _, E = w, J = B, d = C, D += (d ^ E & (J ^ d)) + T[0] - 680876936, D = (D << 7 | D >>> 25) + E << 0, d += (J ^ D & (E ^ J)) + T[1] - 389564586, d = (d << 12 | d >>> 20) + D << 0, J += (E ^ d & (D ^ E)) + T[2] + 606105819, J = (J << 17 | J >>> 15) + d << 0, E += (D ^ J & (d ^ D)) + T[3] - 1044525330, E = (E << 22 | E >>> 10) + J << 0), D += (d ^ E & (J ^ d)) + T[4] - 176418897, D = (D << 7 | D >>> 25) + E << 0, d += (J ^ D & (E ^ J)) + T[5] + 1200080426, d = (d << 12 | d >>> 20) + D << 0, J += (E ^ d & (D ^ E)) + T[6] - 1473231341, J = (J << 17 | J >>> 15) + d << 0, E += (D ^ J & (d ^ D)) + T[7] - 45705983, E = (E << 22 | E >>> 10) + J << 0, D += (d ^ E & (J ^ d)) + T[8] + 1770035416, D = (D << 7 | D >>> 25) + E << 0, d += (J ^ D & (E ^ J)) + T[9] - 1958414417, d = (d << 12 | d >>> 20) + D << 0, J += (E ^ d & (D ^ E)) + T[10] - 42063, J = (J << 17 | J >>> 15) + d << 0, E += (D ^ J & (d ^ D)) + T[11] - 1990404162, E = (E << 22 | E >>> 10) + J << 0, D += (d ^ E & (J ^ d)) + T[12] + 1804603682, D = (D << 7 | D >>> 25) + E << 0, d += (J ^ D & (E ^ J)) + T[13] - 40341101, d = (d << 12 | d >>> 20) + D << 0, J += (E ^ d & (D ^ E)) + T[14] - 1502002290, J = (J << 17 | J >>> 15) + d << 0, E += (D ^ J & (d ^ D)) + T[15] + 1236535329, E = (E << 22 | E >>> 10) + J << 0, D += (J ^ d & (E ^ J)) + T[1] - 165796510, D = (D << 5 | D >>> 27) + E << 0, d += (E ^ J & (D ^ E)) + T[6] - 1069501632, d = (d << 9 | d >>> 23) + D << 0, J += (D ^ E & (d ^ D)) + T[11] + 643717713, J = (J << 14 | J >>> 18) + d << 0, E += (d ^ D & (J ^ d)) + T[0] - 373897302, E = (E << 20 | E >>> 12) + J << 0, D += (J ^ d & (E ^ J)) + T[5] - 701558691, D = (D << 5 | D >>> 27) + E << 0, d += (E ^ J & (D ^ E)) + T[10] + 38016083, d = (d << 9 | d >>> 23) + D << 0, J += (D ^ E & (d ^ D)) + T[15] - 660478335, J = (J << 14 | J >>> 18) + d << 0, E += (d ^ D & (J ^ d)) + T[4] - 405537848, E = (E << 20 | E >>> 12) + J << 0, D += (J ^ d & (E ^ J)) + T[9] + 568446438, D = (D << 5 | D >>> 27) + E << 0, d += (E ^ J & (D ^ E)) + T[14] - 1019803690, d = (d << 9 | d >>> 23) + D << 0, J += (D ^ E & (d ^ D)) + T[3] - 187363961, J = (J << 14 | J >>> 18) + d << 0, E += (d ^ D & (J ^ d)) + T[8] + 1163531501, E = (E << 20 | E >>> 12) + J << 0, D += (J ^ d & (E ^ J)) + T[13] - 1444681467, D = (D << 5 | D >>> 27) + E << 0, d += (E ^ J & (D ^ E)) + T[2] - 51403784, d = (d << 9 | d >>> 23) + D << 0, J += (D ^ E & (d ^ D)) + T[7] + 1735328473, J = (J << 14 | J >>> 18) + d << 0, E += (d ^ D & (J ^ d)) + T[12] - 1926607734, E = (E << 20 | E >>> 12) + J << 0, M = E ^ J, D += (M ^ d) + T[5] - 378558, D = (D << 4 | D >>> 28) + E << 0, d += (M ^ D) + T[8] - 2022574463, d = (d << 11 | d >>> 21) + D << 0, U = d ^ D, J += (U ^ E) + T[11] + 1839030562, J = (J << 16 | J >>> 16) + d << 0, E += (U ^ J) + T[14] - 35309556, E = (E << 23 | E >>> 9) + J << 0, M = E ^ J, D += (M ^ d) + T[1] - 1530992060, D = (D << 4 | D >>> 28) + E << 0, d += (M ^ D) + T[4] + 1272893353, d = (d << 11 | d >>> 21) + D << 0, U = d ^ D, J += (U ^ E) + T[7] - 155497632, J = (J << 16 | J >>> 16) + d << 0, E += (U ^ J) + T[10] - 1094730640, E = (E << 23 | E >>> 9) + J << 0, M = E ^ J, D += (M ^ d) + T[13] + 681279174, D = (D << 4 | D >>> 28) + E << 0, d += (M ^ D) + T[0] - 358537222, d = (d << 11 | d >>> 21) + D << 0, U = d ^ D, J += (U ^ E) + T[3] - 722521979, J = (J << 16 | J >>> 16) + d << 0, E += (U ^ J) + T[6] + 76029189, E = (E << 23 | E >>> 9) + J << 0, M = E ^ J, D += (M ^ d) + T[9] - 640364487, D = (D << 4 | D >>> 28) + E << 0, d += (M ^ D) + T[12] - 421815835, d = (d << 11 | d >>> 21) + D << 0, U = d ^ D, J += (U ^ E) + T[15] + 530742520, J = (J << 16 | J >>> 16) + d << 0, E += (U ^ J) + T[2] - 995338651, E = (E << 23 | E >>> 9) + J << 0,D += (J ^ (E | ~d)) + T[0] - 198630844,D = (D << 6 | D >>> 26) + E << 0,d += (E ^ (D | ~J)) + T[7] + 1126891415,d = (d << 10 | d >>> 22) + D << 0,J += (D ^ (d | ~E)) + T[14] - 1416354905,J = (J << 15 | J >>> 17) + d << 0,E += (d ^ (J | ~D)) + T[5] - 57434055,E = (E << 21 | E >>> 11) + J << 0,D += (J ^ (E | ~d)) + T[12] + 1700485571,D = (D << 6 | D >>> 26) + E << 0,d += (E ^ (D | ~J)) + T[3] - 1894986606,d = (d << 10 | d >>> 22) + D << 0,J += (D ^ (d | ~E)) + T[10] - 1051523,J = (J << 15 | J >>> 17) + d << 0,E += (d ^ (J | ~D)) + T[1] - 2054922799,E = (E << 21 | E >>> 11) + J << 0,D += (J ^ (E | ~d)) + T[8] + 1873313359,D = (D << 6 | D >>> 26) + E << 0,d += (E ^ (D | ~J)) + T[15] - 30611744,d = (d << 10 | d >>> 22) + D << 0,J += (D ^ (d | ~E)) + T[6] - 1560198380,J = (J << 15 | J >>> 17) + d << 0,E += (d ^ (J | ~D)) + T[13] + 1309151649,E = (E << 21 | E >>> 11) + J << 0,D += (J ^ (E | ~d)) + T[4] - 145523070,D = (D << 6 | D >>> 26) + E << 0,d += (E ^ (D | ~J)) + T[11] - 1120210379,d = (d << 10 | d >>> 22) + D << 0,J += (D ^ (d | ~E)) + T[2] + 718787259,J = (J << 15 | J >>> 17) + d << 0,E += (d ^ (J | ~D)) + T[9] - 343485551,E = (E << 21 | E >>> 11) + J << 0,F ? (_ = D + 1732584193 << 0, w = E - 271733879 << 0, B = J - 1732584194 << 0, C = d + 271733878 << 0, F = !1) : (_ = _ + D << 0, w = w + E << 0, B = B + J << 0, C = C + d << 0)
        } while (!H);
        if (A) {
            var G = y[_ >> 4 & 15] + y[15 & _];
            return G += y[_ >> 12 & 15] + y[_ >> 8 & 15], G += y[_ >> 20 & 15] + y[_ >> 16 & 15], G += y[_ >> 28 & 15] + y[_ >> 24 & 15], G += y[w >> 4 & 15] + y[15 & w], G += y[w >> 12 & 15] + y[w >> 8 & 15], G += y[w >> 20 & 15] + y[w >> 16 & 15], G += y[w >> 28 & 15] + y[w >> 24 & 15], G += y[B >> 4 & 15] + y[15 & B], G += y[B >> 12 & 15] + y[B >> 8 & 15], G += y[B >> 20 & 15] + y[B >> 16 & 15], G += y[B >> 28 & 15] + y[B >> 24 & 15], G += y[C >> 4 & 15] + y[15 & C], G += y[C >> 12 & 15] + y[C >> 8 & 15], G += y[C >> 20 & 15] + y[C >> 16 & 15], G += y[C >> 28 & 15] + y[C >> 24 & 15]
        }
        return y[_ >> 4 & 15] + y[15 & _] + y[_ >> 12 & 15] + y[_ >> 8 & 15] + y[_ >> 20 & 15] + y[_ >> 16 & 15] + y[_ >> 28 & 15] + y[_ >> 24 & 15] + y[w >> 4 & 15] + y[15 & w] + y[w >> 12 & 15] + y[w >> 8 & 15] + y[w >> 20 & 15] + y[w >> 16 & 15] + y[w >> 28 & 15] + y[w >> 24 & 15] + y[B >> 4 & 15] + y[15 & B] + y[B >> 12 & 15] + y[B >> 8 & 15] + y[B >> 20 & 15] + y[B >> 16 & 15] + y[B >> 28 & 15] + y[B >> 24 & 15] + y[C >> 4 & 15] + y[15 & C] + y[C >> 12 & 15] + y[C >> 8 & 15] + y[C >> 20 & 15] + y[C >> 16 & 15] + y[C >> 28 & 15] + y[C >> 24 & 15]
    };
    if (!a.JS_MD5_TEST && c) {
        var B = require("crypto"), C = require("buffer").Buffer;
        module.exports = function (a) {
            return "string" == typeof a ? a.length <= 80 ? w(a) : a.length <= 183 && !/[^\x00-\x7F]/.test(a) ? w(a) : B.createHash("md5").update(a, "utf8").digest("hex") : (a.constructor == ArrayBuffer && (a = new Uint8Array(a)), a.length <= 370 ? w(a) : B.createHash("md5").update(new C(a)).digest("hex"))
        }
    } else a && (a.md5 = w)
}(this);
/*!pc/modules/country-code/main.js*/
define("pc/modules/country-code/main", ["require", "exports", "module"], function () {
    function c(c, a) {
        for (var v = c; v[0];) {
            if (v.hasClass(a))return !0;
            v = v.parent()
        }
        return !1
    }

    var a = $(".area_code_list"), v = $(".area_code");
    $(document).on("click", ".area_code", function () {
        return a.is(":visible") ? ($(this).removeClass("active"), a.hide()) : ($(this).addClass("active"), a.show().scrollTop(0)), !1
    }), $(document).on("click", ".area_code_list dd", function () {
        return v.text($(this).children("span").text()), $(".area_code").trigger("click"), !1
    }), $(document).on("click", function (h) {
        var _ = $(h.target);
        return c(_, "area_code_list") ? !1 : (v.removeClass("active"), void a.hide())
    }), $.ajax({
        url: "/register/getPhoneCountryCode.json", success: function (c) {
            var a = "", h = c.content.rows;
            if (v.text(h[0].countryList[0].code), 1 === c.state && h)for (var _ = 0, g = h.length; g > _; _++) {
                a += "<dt>" + h[_].name + "</dt>";
                for (var i = 0,
                         y = h[_].countryList.length; y > i; i++)a += "<dd>" + h[_].countryList[i].name + "<span>" + h[_].countryList[i].code + "</span></dd>"
            } else a = "请求出错";
            $(".code_list_main").append(a)
        }
    })
});
/*!dep/jquery-placeholder/jquery.placeholder.js*/
!function (a) {
    "function" == typeof define && define.amd ? define("dep/jquery-placeholder/jquery.placeholder", ["jquery"], a) : a("object" == typeof module && module.exports ? require("jquery") : jQuery)
}(function (a) {
    function c(c) {
        var h = {}, v = /^jQuery\d+$/;
        return a.each(c.attributes, function (i, a) {
            a.specified && !v.test(a.name) && (h[a.name] = a.value)
        }), h
    }

    function h(c, h) {
        var v = this, b = a(this);
        if (v.value === b.attr(w ? "placeholder-x" : "placeholder") && b.hasClass(H.customClass))if (v.value = "", b.removeClass(H.customClass), b.data("placeholder-password")) {
            if (b = b.hide().nextAll('input[type="password"]:first').show().attr("id", b.removeAttr("id").data("placeholder-id")), c === !0)return b[0].value = h, h;
            b.focus()
        } else v == y() && v.select()
    }

    function v(v) {
        var y, b = this, C = a(this), j = b.id;
        if (!v || "blur" !== v.type || !C.hasClass(H.customClass))if ("" === b.value) {
            if ("password" === b.type) {
                if (!C.data("placeholder-textinput")) {
                    try {
                        y = C.clone().prop({type: "text"})
                    } catch (e) {
                        y = a("<input>").attr(a.extend(c(this), {type: "text"}))
                    }
                    y.removeAttr("name").data({
                        "placeholder-enabled": !0,
                        "placeholder-password": C,
                        "placeholder-id": j
                    }).bind("focus.placeholder", h), C.data({"placeholder-textinput": y, "placeholder-id": j}).before(y)
                }
                b.value = "", C = C.removeAttr("id").hide().prevAll('input[type="text"]:first').attr("id", C.data("placeholder-id")).show()
            } else {
                var A = C.data("placeholder-password");
                A && (A[0].value = "", C.attr("id", C.data("placeholder-id")).show().nextAll('input[type="password"]:last').hide().removeAttr("id"))
            }
            C.addClass(H.customClass), C[0].value = C.attr(w ? "placeholder-x" : "placeholder")
        } else C.removeClass(H.customClass)
    }

    function y() {
        try {
            return document.activeElement
        } catch (a) {
        }
    }

    var b, C, w = !1, j = "[object OperaMini]" === Object.prototype.toString.call(window.operamini),
        A = "placeholder" in document.createElement("input") && !j && !w,
        g = "placeholder" in document.createElement("textarea") && !j && !w, E = a.valHooks, k = a.propHooks, H = {};
    A && g ? (C = a.fn.placeholder = function () {
        return this
    }, C.input = !0, C.textarea = !0) : (C = a.fn.placeholder = function (c) {
        var y = {customClass: "placeholder"};
        return H = a.extend({}, y, c), this.filter((A ? "textarea" : ":input") + "[" + (w ? "placeholder-x" : "placeholder") + "]").not("." + H.customClass).not(":radio, :checkbox, [type=hidden]").bind({
            "focus.placeholder": h,
            "blur.placeholder": v
        }).data("placeholder-enabled", !0).trigger("blur.placeholder")
    }, C.input = A, C.textarea = g, b = {
        get: function (c) {
            var h = a(c), v = h.data("placeholder-password");
            return v ? v[0].value : h.data("placeholder-enabled") && h.hasClass(H.customClass) ? "" : c.value
        }, set: function (c, b) {
            var C, w, j = a(c);
            return "" !== b && (C = j.data("placeholder-textinput"), w = j.data("placeholder-password"), C ? (h.call(C[0], !0, b) || (c.value = b), C[0].value = b) : w && (h.call(c, !0, b) || (w[0].value = b), c.value = b)), j.data("placeholder-enabled") ? ("" === b ? (c.value = b, c != y() && v.call(c)) : (j.hasClass(H.customClass) && h.call(c), c.value = b), j) : (c.value = b, j)
        }
    }, A || (E.input = b, k.value = b), g || (E.textarea = b, k.value = b), a(function () {
        a(document).delegate("form", "submit.placeholder", function () {
            var c = a("." + H.customClass, this).each(function () {
                h.call(this, !0, "")
            });
            setTimeout(function () {
                c.each(v)
            }, 10)
        })
    }), a(window).bind("beforeunload.placeholder", function () {
        var c = !0;
        try {
            "javascript:void(0)" === document.activeElement.toString() && (c = !1)
        } catch (h) {
        }
        c && a("." + H.customClass).each(function () {
            this.value = ""
        })
    }))
});
/*!pc/page/login/main.js*/
define("pc/page/login/main", ["require", "exports", "module", "dep/jquery-placeholder/jquery.placeholder", "pc/modules/country-code/main"], function (require) {
    require("dep/jquery-placeholder/jquery.placeholder"), $("input").placeholder(), require("pc/modules/country-code/main");
    var a = $(".form_body"), F = $(".tab_active"), c = null;
    $(".form_head").on("click", "li", function () {
        var g = $(this), v = g.index();
        0 === v ? $(".divider").removeClass("code_divider") : $(".divider").addClass("code_divider"), g.addClass("active").siblings().removeClass("active"), F.stop().animate({left: g.offsetParent().context.offsetLeft}, 400), a.eq(v).show().siblings(".form_body").hide(), _.setClear(), h.setClear(), clearInterval(c);
        var C = a.eq(v);
        return C.find(".verify_tips_main").hide(), C.find(".auto_phone").removeProp("disabled"), C.find(".verify_tips_count_down").hide(), !1
    });
    var g = {
        1: {message: "成功", linkFor: "username", level: "info"},
        210: {message: "请输入有效的手机/邮箱", linkFor: "username", level: "error"},
        211: {message: "请输入6-16位密码，字母区分大小写", linkFor: "password", level: "error"},
        220: {message: "请输入已验证手机/邮箱", linkFor: "username", level: "error"},
        241: {message: "请输入密码", linkFor: "password", level: "error"},
        400: {message: "帐号和密码不匹配", linkFor: "password", level: "error"},
        10010: {message: "图形验证码不正确", linkFor: "request_form_verifyCode", level: "error"},
        10011: {
            message: "登录错误次数过多，请稍后再试或<a href='https://passport.lagou.com/accountPwd/toReset.html'>重置密码</a>",
            linkFor: "password",
            level: "error"
        },
        10012: {message: "操作过于频繁，请联系管理员", linkFor: "password", level: "error"}
    }, v = {
        1: {message: "验证码已发送，请查收短信", linkFor: "phoneVerificationCode", level: "info"},
        201: {message: "请输入手机号码", linkFor: "username", level: "error"},
        203: {message: "输入号码与归属地不匹配", linkFor: "username", level: "error"},
        204: {message: "系统错误", linkFor: "phoneVerificationCode", level: "error"},
        205: {message: "输入号码与归属地不匹配", linkFor: "username", level: "error"},
        206: {message: "系统错误", linkFor: "phoneVerificationCode", level: "error"},
        207: {message: "该手机获取验证码已达上限，请明天再试", linkFor: "phoneVerificationCode", level: "error"},
        208: {message: "验证码发送太过频繁，请稍后再试", linkFor: "phoneVerificationCode", level: "error"},
        209: {message: "该手机号已被注册", linkFor: "username", level: "error"},
        222: {message: "该手机号未注册", linkFor: "username", level: "error"},
        304: {message: "用户未登录", linkFor: "username", level: "error"},
        402: {message: "获取验证码超时，请稍后再试", linkFor: "phoneVerificationCode", level: "error"},
        10010: {message: "图形验证码不正确", linkFor: "request_form_verifyCode", level: "error"},
        10011: {message: "操作过于频繁，请联系管理员", linkFor: "phoneVerificationCode", level: "error"},
        10012: {message: "操作过于频繁，请联系管理员", linkFor: "phoneVerificationCode", level: "error"}
    }, _ = new lg.Views.BaseView({
        name: "passwordLogin",
        fields: [{
            name: "username",
            validRules: [{mode: "require", data: "", message: "请输入已验证手机/邮箱", trigger: "blur"}, {
                mode: "pattern",
                isUse: !0,
                status: !1,
                data: {
                    phone: /^\d{5,15}$/,
                    email: /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i
                },
                message: "请输入有效的手机/邮箱"
            }],
            controlType: "Phone"
        }, {
            name: "password",
            validRules: [{mode: "require", data: "", message: "请输入密码"}, {
                mode: "pattern",
                data: "/^[\\S\\s]{6,16}$/",
                message: "请输入6-16位密码，字母区分大小写"
            }],
            controlType: "Password"
        }, {
            name: "request_form_verifyCode",
            isVisible: !1,
            validRules: [{mode: "require", data: "", message: "请输入验证码"}, {
                mode: "pattern",
                data: "/^[a-zA-Z0-9一-龥]{4,4}$/",
                message: "请输入正确的验证码"
            }],
            from: "register",
            url: "https://passport.lagou.com/vcode/create",
            controlType: "VerifyCode"
        }, {
            name: "submit", validRules: [], controlType: "Submit", url: "/login/login.json", click: function (e) {
                var a = e, F = a.parent.CollectData(), c = "veenike";
                F.isValidate && (F.password = md5(F.password), F.password = md5(c + F.password + c), $.ajax({
                    url: a.control._option.url,
                    data: F,
                    type: "post",
                    dataType: "json",
                    cache: !1
                }).done(function (F) {
                    if (g[210].message = "请输入有效的手机/邮箱", g[400].message = "帐号和密码不匹配", g[400].linkFor = "password", 1 == F.state) {
                        var c = "/grantServiceTicket/grant.html";
                        return void(window.location.href = c)
                    }
                    g[F.state] ? ($('[data-propertyname="' + g[F.state].linkFor + '"] input').blur(), a.parent.field[g[F.state].linkFor].showMessage({message: g[F.state].message})) : ($('[data-propertyname="password"] input').blur(), a.parent.field.password.showMessage({message: F.message})), a.parent.field.request_form_verifyCode.getVerifyCode()
                }))
            }
        }]
    }), C = $("#isVisiable_request_form_verifyCode").val();
    C && (_.field.request_form_verifyCode.getVerifyCode(), _.field.request_form_verifyCode.setVisible(!0));
    var h = new lg.Views.BaseView({
        name: "codeLogin",
        fields: [{
            name: "username",
            validRules: [{mode: "require", data: "", message: "请输入已验证手机", trigger: "blur"}, {
                mode: "pattern",
                isUse: !0,
                status: !1,
                data: {phone: /^\d{5,11}$/},
                message: "输入号码与归属地不匹配"
            }],
            controlType: "Phone"
        }, {
            name: "request_form_verifyCode",
            validRules: [{mode: "require", data: "", message: "请输入验证码"}, {
                mode: "pattern",
                data: "/^[a-zA-Z0-9一-龥]{4,4}$/",
                message: "请输入正确的验证码"
            }],
            from: "register",
            url: "https://passport.lagou.com/vcode/create",
            controlType: "VerifyCode"
        }, {
            name: "phoneVerificationCode",
            linkFor: "username",
            verifyCode: "request_form_verifyCode",
            totalTips: "该手机获取验证码已达上限，请明天再试",
            validRules: [{mode: "require", data: "", message: "请输入6位数字验证码"}, {
                mode: "pattern",
                isUse: !0,
                status: !1,
                data: "/^[0-9]{6,6}$/",
                message: "请输入6位数字验证码"
            }],
            url: "/login/sendLoginVerifyCode.json",
            controlType: "PhoneVerificationCode",
            click: function (e) {
                var a = e;
                (-1 == a.control.totalTimeTemp || a.control.totalTimeTemp == a.control.getTopTime()) && $.ajax({
                    url: a.control._option.url,
                    data: {
                        countryCode: $('[data-view="codeLogin"] .area_code').text(),
                        phone: a.linkFor.getValue(),
                        type: 0,
                        request_form_verifyCode: lg.Cache.Views[a.control._option.parentName].field.request_form_verifyCode.getValue()
                    },
                    dataType: "json",
                    cache: !1
                }).done(function (F) {
                    var c;
                    return v[F.state] ? a.parent.field[v[F.state].linkFor].showMessage({message: v[F.state].message}) : a.parent.field.phoneVerificationCode.showMessage({message: F.message}), 1 == F.state ? (c = $('[data-propertyname="phoneVerificationCode"]'), $(".verify_tips_main").hide(), void e.control.starttime(e.control, function () {
                        $(".auto_phone").val("语音验证"), $(".verify_tips_main").show(), c.find(".first_child").removeClass("input_warning"), c.children(".input_tips").remove()
                    })) : (e.control.init(), a.parent.field.request_form_verifyCode.getVerifyCode(), void e.control.setDisable(!1))
                })
            }
        }, {
            name: "autoPhoneVerificationCode",
            linkFor: "username",
            verifyCode: "request_form_verifyCode",
            validRules: [],
            url: "/login/sendLoginVerifyCode.json",
            controlType: "PhoneVerificationCode",
            click: function (e) {
                var a = e;
                (-1 == a.control.totalTimeTemp || a.control.totalTimeTemp == a.control.getTopTime()) && $.ajax({
                    url: a.control._option.url,
                    data: {
                        countryCode: $('[data-view="codeLogin"] .area_code').text(),
                        phone: a.linkFor.getValue(),
                        type: 1,
                        request_form_verifyCode: lg.Cache.Views[a.control._option.parentName].field.request_form_verifyCode.getValue()
                    },
                    dataType: "json",
                    cache: !1
                }).done(function (F) {
                    var g, _ = v[F.state], C = a.control.getTopTime();
                    1 === F.state ? (g = $('[data-propertyname="phoneVerificationCode"]'), g.find(".last_child").addClass("btn_disabled").prop("disabled", !0), clearInterval(c), c = setInterval(function () {
                        --C < 0 ? (clearInterval(c), g.find(".first_child").removeClass("input_warning"), g.find(".last_child").removeClass("btn_disabled").removeProp("disabled"), $(".auto_phone").removeProp("disabled"), $(".verify_tips_count_down").hide(), $(".verify_tips_main").show(), e.control.init()) : (C === a.control.getTopTime() - 1 && $(".verify_tips_main").hide(), $(".verify_tips_count_down").html("请留意接收手机来电，" + C + "秒后可重试…").show())
                    }, 1e3)) : (e.control.init(), _ ? a.parent.field[_.linkFor].showMessage({message: _.message}) : a.parent.field.phoneVerificationCode.showMessage({message: F.message}), a.parent.field.request_form_verifyCode.getVerifyCode()), e.control.setDisable(!1)
                })
            }
        }, {
            name: "submit", validRules: [], controlType: "Submit", url: "/login/login.json", click: function (e) {
                var a = e, F = a.parent.CollectData();
                F.countryCode = $('[data-view="codeLogin"] .area_code').text(), F.isValidate && $.ajax({
                    url: a.control._option.url,
                    data: F,
                    type: "post",
                    dataType: "json",
                    cache: !1
                }).done(function (F) {
                    if (g[210].message = "输入号码与归属地不匹配", g[400].message = "帐号和验证码不匹配", g[400].linkFor = "phoneVerificationCode", 1 == F.state) {
                        var c = "/grantServiceTicket/grant.html";
                        return void(window.location.href = c)
                    }
                    g[F.state] ? ($('[data-propertyname="' + g[F.state].linkFor + '"] input').blur(), a.parent.field[g[F.state].linkFor].showMessage({message: g[F.state].message})) : ($('[data-propertyname="phoneVerificationCode"] input').blur(), a.parent.field.phoneVerificationCode.showMessage({message: F.message})), a.parent.field.request_form_verifyCode.getVerifyCode()
                })
            }
        }]
    });
    h.field.request_form_verifyCode.getVerifyCode()
});
/*!pc/modules/event/happy-3rd-birthday/main.js*/
define("pc/modules/event/happy-3rd-birthday/main", ["require", "exports", "module"], function () {
    var a = $("#serverTime").val();
    if (a) {
        {
            var h = new Date(parseInt(a)), w = new Date("2016/07/20 23:59:59");
            new Date("2016/07/31 23:59:59")
        }
        w >= h && $(".sso_header .logo").attr("href", "http://www.lagou.com/topic/3years.html")
    }
});