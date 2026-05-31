function apiPost(url, data={}, done_callback=function(){ }, fail_callback=function(){ }, debug=false){
    $.ajax({
        dataType    : 'json',
        method      : 'POST',
        contentType : 'application/x-www-form-urlencoded; charset=UTF-8',
        data        : data,
        url         : BASEURL + '/' + url+ '?lang='+language+'&game='+game+'&army='+army,        
    }).done(done_callback).fail(fail_callback);    
}

function showPicture(name){
    name = name.replace(/ /g, '_');
    if(name=="")return;
    $('picture').css('background-image', `url('${name}')`);
    $('picture').addClass('active');    
}

function hidePicture(){
    $('picture').css('background-image', 'none');
    $('picture').removeClass('active');    
}
