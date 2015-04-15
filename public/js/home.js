$(document).ready(function(){
	$('.panic-div').hide();
	$('.home-btn').click(function(){
		$('.home-btn').toggleClass('btn-success');
		$('.home-btn').toggleClass('btn-danger');
		$('.panic-div').toggle();
	})
});