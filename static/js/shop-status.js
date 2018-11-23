/**
 * Created by tarena on 18-11-18.
 */

function check_login(){
    $.get('/check_login/',function(data){
        var html = "";
        if (data.status == 0){
            html+="<h4>登入后才能购物</h4>";
            html+="<a href='/login'>[登入]</a>  ";
            html+="<a href='/register'>[没有账号]</a>";
        }else if(data.status ==1){
            user = JSON.parse(data.user)
            html+="<h2>欢迎:"+user.username+"&nbsp;&nbsp;</h2>";
            html+="<a href='/logout/'>退出账号</a>";
        }
        $("#dengruzhuantai").html(html);
    },'json');
}


$(function(){
    check_login();
});