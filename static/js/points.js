/**
 * Created by tarena on 18-11-17.
 */

/* 这个js文件是关于index页面地图的  */
var map = new BMap.Map("container");//创建地图
var point = new BMap.Point(113.2603311539,23.1196799985);//创建地图坐标点,一般首次创建的这个点为地图的中心坐标点
map.centerAndZoom(point,15);//初始化地图，设置中心坐标点和地图级数
var marker = new BMap.Marker(point);
map.enableScrollWheelZoom(true);

marker.enableDragging();

var i=0;

function get_stores(){
    $.ajaxSettings.async = false;
    window.storeList='a';  //创建全局变量用于提取从后端提取的数据data
    $.get('/get_stores/',function(data){window.storeList=data},'json');//data为后端get_stores_views()函数的返回值
    return window.storeList;

}
var storeList = get_stores();

function markerFun (points,dic) {
    var markers = new BMap.Marker(points);
    map.addOverlay(markers);
    markers.addEventListener("click", function(){
        // parent.location.href='cart/';
        var storename = dic.name;
        var storeid = dic.id;
        $.ajax({
            url:'/cart/',
            type:'post',
            data:{
                storename:storename,
                storeid:storeid,
                csrfmiddlewaretoken:$
                ("[name='csrfmiddlewaretoken']").val()
            },
            async:false,
            dataType:'json',
            success:function(result){}
        });
        parent.location.href='cart/';
    });
}

function Laber(points,sdk) {
    var opts = {
          position:points,
          offset:new BMap.Size(-10)
      };
    var label = new BMap.Label("开心购:"+sdk, opts);  // 创建文本标注对象
        label.setStyle({
         color : "red",
         fontSize : "12px",
         height : "20px",
         lineHeight : "20px",
         fontFamily:"华文行楷"
     });
      map.addOverlay(label);
}
function Gc(pointds) {
    var point = new BMap.Point(pointds);
    var gc = new BMap.Geocoder();
    gc.getLocation(point,function (rs) {
        var addComp = rs.addressComponents;
        alert(addComp.province+","+addComp.city+","+addComp.district
        +","+addComp.street+","+addComp.streetNumber);
    });
}

for (i;i<window.storeList.length;i++){
    var dic = JSON.parse(window.storeList[i]);
    var points = new BMap.Point(dic.x,dic.y);
    var storeid = dic.id;
    // console.log(storeid)
    markerFun(points,dic);
    Laber(points,dic.name)
}

