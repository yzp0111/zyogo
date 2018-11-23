/**
 * Created by tarena on 18-11-12.
 */
function checkUphone(){
    var value = $("[name='uphone']").val();
    window.flag = false;
    if(/^1[34578]\d{9}$/.test(value)){
        //验证手机号码是否存在
        $.ajax({
            url:'/check_uphone/',
            type:'post',
            data:{
                uphone:value,
                csrfmiddlewaretoken:$
                ("[name='csrfmiddlewaretoken']").val()
            },
            async:false,
            dataType:'json',
            success:function(data){
                $('#uphone-show').html(data.text);
                if(data.status == 1)
                    window.flag = true;
                else
                    window.flag = false;
            }
        });
    }else{
        $("#uphone-show").html('手机号码不符合规范');
        window.flag = false;
    }
    return window.flag
}

function checkPassword(){
    var upwd = $("[name='password']").val();
    if(upwd.length>=6 && upwd.length<=15){
        $('#password-show').html('');
        return true;
    }else{
        $('#password-show').html('密码不符合规范');
        return false;
    }
}

function checkCpassword(){
    var upwd = $("[name='password']").val();
    var cpwd = $("[name='cpassword']").val();
    if(upwd == cpwd){
        $('#cpassword-show').html('');
        return true;
    }else{
        $('#cpassword-show').html('两次密码输入不同');
        return false;
    }
}

function checkUname(){
    var uname = $("[name='username']").val();
    if(uname){
        $('#uname-show').html('');
        return true;
    }else{
        $('#uname-show').html('昵称不能为空');
        return false;
    }
}

$(function(){
    $("[name='uphone']").blur(function(){
        checkUphone();
    });
    $("[name='password']").blur(function(){
        checkPassword();
    });
    $("[name='cpassword']").blur(function(){
        checkCpassword();
    });
    $("[name='username']").blur(function(){
        checkUname();
    });
    $("#frmRegister").submit(function(){
        return checkUphone() && checkPassword() && checkCpassword() && checkUname();
    });
});