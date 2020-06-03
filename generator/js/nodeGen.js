'use strict'
let log = console.log.bind(console);

$(document).ready(function () {
	const nodeTemplate=$($('#nodeTemplate').html());
	const wallTemplate=$($('#wallTemplate').html());
	
	let nodeCount=0;	//not actual count but unique cumulative identifiers
	let wallCount=0;
	var nodes=new Set();
	
	function setWallListeners(nodeId,wallId){
		$("#"+wallId).find('.button_deleteWall').click(function(){
			$("#"+wallId).remove();
		});
		
		$("#"+wallId).find('.button_duplicateWall').click(function(){
			let idToDuplicate=wallId;
			wallCount++;
			let duplicateId='wall'+wallCount;
			$("#"+nodeId).find('.wallForm').append($("#"+idToDuplicate).clone().attr('id',duplicateId));
			setWallListeners(nodeId,duplicateId);
		});
	}
	
	$("#button_addNode").click(function(){
		nodeCount++;
		let nodeId='node'+nodeCount;
		log(nodeId);
		$("#nodeForm").append(nodeTemplate.clone().attr('id',nodeId));
		
		$("#"+nodeId).find('.button_addWall').click(function(){
			wallCount++;
			let wallId='wall'+wallCount;
			$("#"+nodeId).find('.wallForm').append(wallTemplate.clone().attr('id',wallId));
			setWallListeners(nodeId,wallId);
		});
		
		$("#"+nodeId).find('.button_deleteNode').click(function(){
			$("#"+nodeId).remove();
		});
		
		// not trivial- todo when bored
		// $("#"+nodeId).find('.button_duplicateNode').click(function(){
			// log("clicked!");
			// wallCount++;
			// let wallId='wall'+wallCount;
			// $("#"+nodeId).find('.wallForm').append(wallTemplate.clone().attr('id',wallId));
			// setWallListeners(nodeId,wallId);
		// });
	});
	
	$("#button_generate").click(function(){
		log("generating--");
		let output=[];
		output.push({
				id : "0",
				roomtype : "outside",
				floorArea : "",
				innerWalls : []
			});
		
		let idCount=1;
		$('#nodeForm').children('.row').each(function(){
			let node={
				id : (idCount++).toString(),//$(this).find('.input_id').val(),
				roomtype : $(this).find('.input_roomtype').val(),
				floorArea : $(this).find('.input_area').val(),
				innerWalls : []
			}
			$(this).find('.wallForm').children('.wall').each(function () {
				var v1 = $(this).find('.input_v1').val().split(',',2);
				var v2 = $(this).find('.input_v2').val().split(',',2);
				let wall={
					material : $(this).find('.input_material').val(),
					wallType : $(this).find('.input_wallType').val(),
					vertices : [v1,v2],
					wallLength : $(this).find('.input_wallLength').val(),
					wallArea : $(this).find('.input_wallArea').val(),
					thickness : $(this).find('.input_thickness').val()
				}
				// if(!$(this).find('.input_isInfill').is(":checked"))
					// wall['isStructural']=$(this).find('.input_isStructural').is(":checked");
				//wall['isOn']=true;
				node.innerWalls.push(wall);
				//alert(this.value); // "this" is the current element in the loop
			});
			output.push(node);
		});
		
		$("#output").val(JSON.stringify(output));
	});
});