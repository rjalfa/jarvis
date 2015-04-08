$(document).ready(function(){
	showMax();
});

function showMax()
{
	$.get("/showData", function(data, status){
        if(Number(data) > 40) $(".temp").css({"color":"red"});
        else $(".temp").css({"color":"blue"});
        $(".temp").html(data+" °C");
        setTimeout(showMax, 300);
    });
}