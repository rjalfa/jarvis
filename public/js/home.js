panic = false;
$(document).ready(function(){
	$('.panic-div').hide();
	$('.home-btn').click(function(){
		$('.home-btn').toggleClass('btn-success');
		$('.home-btn').toggleClass('btn-danger');
		$('.panic-div').toggle();
		if($('.home-btn').hasClass("btn-danger")) panic = true;
		else panic = false;
		setPanic();
	})
});

function setPanic()
{
	$.post("/setPanic",{'p':panic.toString()});
}