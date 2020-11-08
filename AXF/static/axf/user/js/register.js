// 检查用户名是否存在事件
$(function () {

    var $username = $("#username_input");

    $username.change(function () {

        var username = $username.val().trim();

        if (username.length) {

            // 将用户名发送给服务器进行预效验
            $.getJSON('/axf/checkuser/', {'username': username}, function (data) {

                console.log(data);

                var $username_info = $("#username_info");

                if (data['status'] === 200) {
                    $username_info.html("用户名可用").css("color", 'green');
                } else if (data['status'] === 901) {
                    $username_info.html("用户已存在").css('color', 'red');
                }
            })
        } else {
            var $username_info = $("#username_info");
            $username_info.html("用户名不能为空").css("color", 'red');
        }
    })
})

// 检查邮箱是否存在事件
$(function () {

    var $email = $("#email_input");

    $email.change(function () {

        var email = $email.val().trim();

        if (email.length) {

            // 将用户名发送给服务器进行预效验
            $.getJSON('/axf/checkemail/', {'email': email}, function (data) {

                console.log(data);

                var $email_info = $("#email_info");

                if (data['status'] === 200) {
                    $email_info.html("邮箱可用").css("color", 'green');
                } else if (data['status'] === 901) {
                    $email_info.html("邮箱已存在").css('color', 'red');
                }
            })
        } else {
            var $email_info = $("#email_info");
            $email_info.html("邮箱不能为空").css("color", 'red');
        }
    })
})

// 检查两次密码输入是否一致事件
$(function () {
    var $password_input = $("#password_input")
    var $password_confirm_input = $("#password_confirm_input")

    $password_confirm_input.change(function () {
        var password_input = $password_input.val();
        var password_confirm_input = $password_confirm_input.val();
        var $password_confirm_info = $("#password_confirm_info");
        var $password_input_info = $("#password_input_info");
        if (password_input === password_confirm_input) {
            $password_confirm_info.html('');
            $password_input_info.html('');
        } else if (password_confirm_input && !password_input) {
            $password_confirm_info.html('');
        } else if (password_input !== password_confirm_input) {
            $password_confirm_info.html('两次密码输入不一致').css('color', 'red');
            $password_input_info.html('两次密码输入不一致').css('color', 'red');
        }
    })
    $password_input.change(function () {
        var password_input = $password_input.val();
        var password_confirm_input = $password_confirm_input.val();
        var $password_confirm_info = $("#password_confirm_info");
        var $password_input_info = $("#password_input_info");
        if (password_input === password_confirm_input) {
            $password_confirm_info.html('');
            $password_input_info.html('');
        } else if (password_input && !password_confirm_input) {
            $password_input_info.html('');
        } else if (password_input !== password_confirm_input) {
            $password_confirm_info.html('两次密码输入不一致').css('color', 'red');
            $password_input_info.html('两次密码输入不一致').css('color', 'red');
        }
    })
})

// 判断页面是否可提交方法
function check() {
    var $username = $("#username_input");
    var username = $username.val().trim();
    if (!username) {
        var $username_info = $("#username_info");
        $username_info.html("用户名不能为空").css("color", 'red');
        console.log('用户名不能为空');
        return false
    }

    var $email = $("#email_input");
    var email = $email.val().trim();
    if (!email) {
        var $email_info = $("#email_info");
        $email_info.html("邮箱不能为空").css("color", 'red');
        console.log('邮箱不能为空');
        return false
    }


    var $password_input = $("#password_input");
    var password_input = $password_input.val().trim();
    var $password_confirm_input = $("#password_confirm_input");
    var password_confirm_input = $password_confirm_input.val().trim();
    var $password_input_info = $("#password_input_info");
    var $password_confirm_info = $("#password_confirm_info");
    if (!password_input) {
        $password_input_info.html('密码不能为空').css("color", 'red');
        return false
    } else if (!password_confirm_input) {
        $password_confirm_info.html("密码不能为空").css("color", 'red');
        return false
    }


    var username_color = $("#username_info").css('color');
    console.log(username_color);
    if (username_color == 'rgb(255, 0, 0)') {
        return false
    } else {

        var $password_input = $("#password_input");

        var password = $password_input.val().trim();

        $password_input.val(md5(password));

        var password_confirm_input = $("#password_confirm_input");

        var password_confirm = password_confirm_input.val().trim();

        $password_confirm_input.val(md5(password_confirm));

        return true
    }

    var password_input_color = $("#password_input_info").css('color');
    console.log(password_input_color);
    if (password_input_color == 'rgb(255, 0, 0)') {
        return false
    }

    var password_confirm_color = $("#password_confirm_info").css('color');
    console.log(password_confirm_color);
    if (password_confirm_color == 'rgb(255, 0, 0)') {
        return false
    }


}