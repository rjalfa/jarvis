$(document).ready(function(){
	showMax();
});

function showMax()
{
	$.get("/showData", function(data, status){
        //if(Number(data) > 40) $(".temp").css({"color":"red"});
        //else $(".temp").css({"color":"blue"});
        var low = 0,high = 50;
        var temp = Number(data['temp']);
        var R = 0,B = 0;
        if(temp<low) B = 255;
        else if(temp>high) R = 255;
        else {
        	R = Math.round((temp-low)*255.0/(high-low));
        	B = Math.round((high-temp)*255.0/(high-low));
        }
        $(".temp").css({"color":rgbToHex(R,0,B)});
        $(".temp").html(data['temp']+" °C");
        $(".humid").html("Humidity: "+data['humid']+" %");
        setTimeout(showMax, 300);
    },'json');
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}