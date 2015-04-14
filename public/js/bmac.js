$(document).ready(function(){
	$.post("/getbmac",function(req,res){
		$(".macs").html(req);
	});
});