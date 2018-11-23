/**
 * Created by tarena on 18-11-17.
 */


// function get_stores(){
//     $.ajaxSettings.async = false;
//     window.winList='a';  //创建全局变量用于提取从后端提取的数据data
//     $.get('/get_windows/',function(data){window.winList=data},'json');//data为后端get_stores_views()函数的返回值
//     return window.winList;
// }
//
// var storeList = get_stores();

function get_stores(){
    console.log("-------------");
    $.get('/get_windows/',function(data){
        console.log("---=======-----");
        //循环遍历data
        var html = '';
        $.each(data,function(i,obj){
            var dic = JSON.parse(obj);
            html += '<div class="col-sm-4">';
            html += '<div class="ct-product">';
            html += '<div class="image"><img src="/'+ dic.goodspicture + '" alt=""></div>';
            html += '<div class="inner"><a href="#" class="btn btn-motive ct-product-button"><i class="fa fa-shopping-cart"></i></a>';
            html += '<h2 class="ct-product-title">' + dic.goodsname + '</h2>';
            html += '<p class="ct-product-description">剩余商品数量:'+ dic.goodsnumber +'件</p>';
            html += '<span class="ct-product-price">￥' + dic.goodsprice + '</span>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
        });
        console.log(html)
        $("#maincart").html(html);
    },'json');//data为后端get_stores_views()函数的返回值
}

$(function(){
    console.log("++++++++++++")
    get_stores();
    console.log("+========+")
});

// function show_windows(){
//     var html = '';
//     html += '<div class="col-sm-4">';
//     html += '<div class="image"><img src="/'+ dic.goodspicture + '" alt=""></div>';
//     html += '<div class="inner"><a href="#" class="btn btn-motive ct-product-button"><i class="fa fa-shopping-cart"></i></a>';
//     html += '<h2 class="ct-product-title">' + dic.goodsname + '</h2>';
//     html += '<p class="ct-product-description">剩余商品数量:'+ dic.goodsnumber +'件</p>';
//     html += '<span class="ct-product-price">￥' + dic.goodsprice + '</span>';
//     html += '</div>';
//     html += '</div>';
//     html += '</div>';
// }
//
// for (i;i<window.winList.length;i++){
//     var dic = JSON.parse(window.winList[i]);
//     var storeid = dic.id;
// }





// <div class="col-sm-4">
//   <div class="ct-product">
//     <div class="image"><img src="/static/images/product-03.jpg" alt=""></div>
//     <div class="inner"><a href="#" class="btn btn-motive ct-product-button"><i class="fa fa-shopping-cart"></i></a>
//       <h2 class="ct-product-title">Coffee Macaroons</h2>
//       <p class="ct-product-description">A very delicious macaroons ...</p><span class="ct-product-price">$59.99</span>
//     </div>
//   </div>
// </div>