
function tobool(string){
	if(string == "true") return true;
	return false;
}

var flag = false;

$(document).ready(function(){
	$("[name='my-checkbox']").bootstrapSwitch();
	$.post('/showApp',function(req,res) {
		$("#box1").bootstrapSwitch('state',req[0],true);
		$("#box2").bootstrapSwitch('state',req[1],true);
		$("#box3").bootstrapSwitch('state',req[2],true);
		$("#box4").bootstrapSwitch('state',req[3],true);
		flag = true;
	});
	$("[name='my-checkbox']").on('switchChange.bootstrapSwitch',function(){
		if(flag) $.post('/postApp',{"0":$("#box1").bootstrapSwitch('state'),"1":$("#box2").bootstrapSwitch('state'),"2":$("#box3").bootstrapSwitch('state'),"3":$("#box4").bootstrapSwitch('state')},function(data,status,xhr){
		},"json");
	});
});