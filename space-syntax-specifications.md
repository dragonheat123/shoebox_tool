# Space Syntax Graph Specification (Updated 2020/06/05)
This document specifies technical specifications of space syntax developed to for unit parcelation and Global Warning Potential calculation. For an overview on how to use the tool itself [see here](../README.md).

## Dependencies:
- jsonpickle (to be removed)
- pandas
- more_itertools
- sortedcontainers

## Inputs:
Two main inputs are required to construct a space syntax graph:
- list of nodes
- list of edges (corresponds to nodes)

Note the floor thickness, height and number of floors are independant and stored in building definition instead.
Data structure in json follows
### Nodes
```js
[
	{
		"id":"0",		//id 0 is reserved for outside node
		"roomType":"outside",
		"floorArea":"",
		"floorMatId":"CP032",
		"innerWalls":[]	//placeholder for future reuquirements
	},
	{
		"id":"1",
		"roomType":"service",
		"floorArea":"",
		"floorMatId":"CP032",
		"innerWalls":[]
	},
	{
		"id":"2",
		"roomType":"normal",
		"floorArea":"",
		"floorMatId":"CP032",
		"innerWalls":[]
	}
]
```
### Edges
```js
[
	{
		"edgeId":"0/2",
		"isAccessible":false,   //isTraversable edge
		"adjWalls":[    
				{
					"matId":["CP024","CP032"],				// id from lcadb [0]=>structural [1]=>infill
					"vertices":[[0,0],[0,1]],   // [x1,y1],[x2,y2]
					"thickness":"1",
					"composition":[0.1,0.9]		// [0]=>structural [1]=>infill
				},
				{
					"matId":["CP024","CP032"],
					"vertices":[[0,1],[1,1]],
					"thickness":"1",
					"composition":[0.1,0.9]
				}
			]
	},	
	{
		"edgeId":"0/1",
		"isAccessible":false,
		"adjWalls":[
				{
					"matId":["CP024",""],
					"vertices":[[2,4],[4,4]],
					"thickness":"1",
					"composition":[1,0]
				}
			]
	},
	{
		"edgeId":"1/2",
		"isAccessible":true,
		"adjWalls":[
				{
					"matId":["CP024","CP032"],
					"vertices":[[5,5],[6,6]],
					"thickness":"1",
					"composition":[0.8,0.2]
				}
			]
	}
]
```
#### Old wall definition (for reference)
```js
{
	"material":"cement",
	"vertices":[[0,1],[1,1]],
	"wallLength":"1",
	"wallArea":"2",
	"thickness":"1",
	"isStructural":true
}
```
