
$(document).ready(function(){
	$("[name='my-checkbox']").bootstrapSwitch();
	/*$.post('/showApp',function(req,res){
		
	})*/
	$("[name='my-checkbox']").on('switchChange.bootstrapSwitch',function(){
		$.post('/postApp',{"0":$("#box1").bootstrapSwitch('state'),"1":$("#box2").bootstrapSwitch('state'),"2":$("#box3").bootstrapSwitch('state'),"3":$("#box4").bootstrapSwitch('state')},function(data,status,xhr){
		},"json");
	});
});