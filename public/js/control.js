$(document).ready(function(){
	$("[name='my-checkbox']").bootstrapSwitch();
	$("#box1").change(dataHandler);
});

function dataHandler()
{
	alert("changed value");
}