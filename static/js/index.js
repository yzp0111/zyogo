/**
 * Created by tarena on 18-11-13.
 */

//根据用户登入状态显示主界面顶行信息
function check_login(){
    $.get('/check_login/',function(data){
        var html = "";
        if (data.status == 0){
            html+="<a href='/login'>[登入]</a>&nbsp;&nbsp;";
            html+="<a href='/register'>[注册有惊喜]</a>"
        }else if(data.status ==1){
            user = JSON.parse(data.user)
            html+="欢迎:"+user.username+"&nbsp;&nbsp;";
            html+="<a href='/logout/'>退出</a>"
        }
        $("#list>li:first").html(html);
    },'json');
}


$(function(){
    check_login();
});