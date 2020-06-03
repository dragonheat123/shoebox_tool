'use strict'
let log = console.log.bind(console);

$(document).ready(function () {
	let edgeTemplate=$($('#edgeTemplate').html());
	const wallTemplate=$($('#wallTemplate').html());
	
	let edgeCount=0;
	let wallCount=0;
	let nodeSet=new Set();
	let nodeSel=[];
	
	$('#input').keyup(function(){
		try{
			let nodes=JSON.parse($(this).val());
			nodeSet.clear();
			nodeSel=[];
			for (let x=0; x<nodes.length; x++){
				nodeSel[nodes[x].id]=nodes[x].roomtype;
				nodeSet.add(nodes[x].id);
			}
			updateSelection($('.input_node1, .input_node2'));
			updateSelection($(edgeTemplate.find('.input_node1, .input_node2')));
		}
		catch(err){
			log("parse failed");
		}
		log(nodeSet);
	});
	
	function updateSelection(sel){
		// let sel=$('.input_node1, .input_node2');
		// TODO: show roomtype for clarity
		sel.empty();

		for (var nodeId in nodeSel) {
			// skip loop if the property is from prototype
			if (!nodeSel.hasOwnProperty(nodeId)) continue;
			let roomtype = nodeSel[nodeId];
			sel.append($("<option></option>").attr("value", nodeId).text(nodeId+": "+nodeSel[nodeId]));
		}

		// nodeSet.forEach(function(node){
			// sel.append($("<option></option>").attr("value", node).text(node));
			// log(node);
		// });
		//sel.append($("<option></option>").attr("value", "outside").text("Outside"));
		
		log("selection updated");
	}
	
	function setWallListeners(edgeId,wallId){
		$("#"+wallId).find('.button_deleteWall').click(function(){
			$("#"+wallId).remove();
		});
		
		$("#"+wallId).find('.button_duplicateWall').click(function(){
			let idToDuplicate=wallId;
			wallCount++;
			let duplicateId='wall'+wallCount;
			$("#"+edgeId).find('.wallForm').append($("#"+idToDuplicate).clone().attr('id',duplicateId));
			setWallListeners(edgeId,duplicateId);
		});
	}
	
	$("#button_addEdge").click(function(){
		edgeCount++;
		let edgeId='edge'+edgeCount;
		$("#edgeForm").append(edgeTemplate.clone().attr('id',edgeId));
		
		$("#"+edgeId).find('.button_deleteEdge').click(function(){
			$("#"+edgeId).remove();
		});
		
		$("#"+edgeId).find('.button_addWall').click(function(){
			wallCount++;
			let wallId='wall'+wallCount;
			$("#"+edgeId).find('.wallForm').append(wallTemplate.clone().attr('id',wallId));
			setWallListeners(edgeId,wallId);
		});
		
		$("#"+edgeId).find('.button_deleteNode').click(function(){
			$("#"+edgeId).remove();
		});		
	});
	
	$("#button_generate").click(function(){
		log("generating--");
		let output=[];
		
		$('#edgeForm').children('.row').each(function(){
			
			let nodes=[$(this).find('.input_node1').val(),$(this).find('.input_node2').val()];
			nodes.sort();
			let edge={
				edgeId : nodes[0]+'/'+nodes[1],
				nodes : nodes,
				isAccessible : $(this).find('.input_isAccessible').is(":checked"),
				isDoorway : $(this).find('.input_isDoorway').is(":checked"),
				adjWalls : []
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
				edge.adjWalls.push(wall);
				//alert(this.value); // "this" is the current element in the loop
			});
			output.push(edge);
		});
		
		$("#output").val(JSON.stringify(output));
	});
});