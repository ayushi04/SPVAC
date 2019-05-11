//THIS CODE ASSUMES THAT INPUT IS CSV
// FIRST ROW REPRESENTS COLUMN-NAMES

//INPUT PARAMETER FROM MAIN METHOD, GLOBAL AND WIDELY USED IN ALMOST ALL FUNCTIONS
var datasetPath=''; //WILL BE USED ONLY ONCE, LEFT FOR LATER REFERENCE OR SYMMETRY OF CODE
var order='';
var classColumn='';
var colorDict={};
var container;

var allData,columnNames,total,classLabel;
var min,max;

var vis,visWidth;
var w,h,r,p=20,k;
var inner_radius,outer_radius;

var selectedColumn='';
var x_scale = d3.scale.linear().range([0, 360]);
var x_scale_rev=d3.scale.linear().domain([0,360]);


var arc = function(c,count,prev) {
    var i=10;


    return d3.svg.arc()
    .innerRadius(function(d) {
	    var k1=0;
	    var k_dash=(outer_radius-inner_radius)/d.length;
        for(var k2=0;k2<d.length;k2++) {
        	if(prev.has(d[k2][columnNames[classColumn]]))
        		k1+=1;
        }
    	return inner_radius + k_dash*k1*1;
    })
    .outerRadius(function(d) {
        var k1=0;
	    var k_dash=(outer_radius-inner_radius)/d.length;
        for(var k2=0;k2<d.length;k2++) {
        	if(d[k2][columnNames[classColumn]]==c || prev.has(d[k2][columnNames[classColumn]]))
        		k1+=1;
        }
        //console.log(inner_radius,k*k1*5 + inner_radius);
        //console.log(k,total,3*Math.sqrt((36*k*d.length)/Math.PI + inner_radius*inner_radius));
        return k_dash*k1*1 + inner_radius;
        //return Math.sqrt((36*k*d.length)/Math.PI + inner_radius*inner_radius);
        //return inner_radius+d.length*5;
        })
    .startAngle(function(d,i) { return (i*10) * (Math.PI/180);}) //converting from degs to radians
    .endAngle(function(d,i) {return (i*10 + 10) * (Math.PI/180);});
};

function createGiantWheel(data,columnNames) {
  console.log('createGiantWheel');
	// The main SVG visualization element
    var container='#windrose'
    vis = d3.select(container)
        .append("svg:svg")
        .attr("width", w + "px").attr("height", (h + 30) + "px");


	var ring_width=(w/2-50)/(order.length);
	var ring=d3.range(50,w/2+1,ring_width);
	vis.append("svg:g")
		.attr("class", "axes")
		.selectAll("circle")
		.data(ring)
		.enter().append("svg:circle")
		.attr("cx", r).attr("cy", r).attr("fill","#044B94").attr("fill-opacity","0.05")
		.attr("r", function(d) { return d; });



    selectedColumn=order[0];
    for(var x=0; x<(ring.length-1);x++) {
    	inner_radius=ring[x];
    	outer_radius=ring[x+1];
    	selectedColumn=order[x];
	    k=(outer_radius-inner_radius)/total;

	    min = d3.min(data, function(d) { return d[columnNames[selectedColumn]]; });
	    max = d3.max(data, function(d) { return d[columnNames[selectedColumn]]; });
      console.log(min,max);
	    var bins=d3.layout.histogram() //DIVIDING DATASET IN 36 BINS
	                      .bins(36)
	                      .range([min,max]) //CHECK +1 not sure, might need to remove
	                      .value(function(d) { return d[columnNames[selectedColumn]]; })
	                      (data);
	    classLabel=data.map( function(data){return data[columnNames[classColumn]];} );
	    classLabel = new Set(classLabel);

	    x_scale_rev.range(d3.extent(data, function(d) { return d[columnNames[x]]; })).nice();

        drawComplexArcs(vis, bins);
    }

    for(var x=0; x<(ring.length-1);x++) {

        inner_radius=ring[x];
        outer_radius=ring[x+1];
        selectedColumn=order[x];
        k=(outer_radius-inner_radius)/total;
        console.log(selectedColumn);
        min = d3.min(data, function(d) { return d[columnNames[selectedColumn]]; });
        max = d3.max(data, function(d) { return d[columnNames[selectedColumn]]; });
        var bins=d3.layout.histogram() //DIVIDING DATASET IN 36 BINS
                          .bins(36)
                          .range([min,max]) //CHECK +1 not sure, might need to remove
                          .value(function(d) { return d[columnNames[selectedColumn]]; })
                          (data);
        classLabel=data.map( function(data){return data[columnNames[classColumn]];} );
        classLabel = new Set(classLabel);

        x_scale_rev.range(d3.extent(data, function(d) { return d[columnNames[order[x]]]; })).nice();

	    vis.append("svg:g")
        .attr("class", "labels")
        .selectAll("text")
        .data(d3.range(0, 351, 30))
        .enter().append("svg:text")
        .attr("dy", "-4px")
        .attr("transform", function(d) {
        var p1=outer_radius-ring_width/2;
        	p1=w/2-p1;
        	return "translate(" + r + "," + p1 + ") rotate(" + d + ",0," + (r-p1) + ")"})

        //.attr("transform", "translate(" + visWidth+inner_radius + "," + visWidth + ")")
        .text(function(dir) { return x_scale_rev(dir).toFixed(2); });
	}


    outer_radius=w/2;
    inner_radius=50;
    k=(outer_radius-inner_radius)/total;

    vis.selectAll('.line')
        .data(d3.range(0,351,10))
        .enter()
        .append("svg:line")
        .attr("x1", function(d) {return r+ (outer_radius)*Math.cos(d*(Math.PI/180));})
        .attr("y1", function(d) {return r+ (outer_radius)*Math.sin(d*(Math.PI/180));})
        .attr("x2", function(d) {return r+(inner_radius)*Math.cos(d*(Math.PI/180));})
        .attr("y2", function(d) {return r+(inner_radius)*Math.sin(d*(Math.PI/180));})
        .attr("stroke-width", 0.5)
        .attr("stroke", "black");

}

// Draw a complete wind rose visualization, including axes and center text
function drawComplexArcs(parent, plotData) {
    var count=0;
    var prev=new Set();
    for (let c of classLabel) {
        count+=1;
        parent.append("svg:g")
            .attr("class", "arcs")
            .selectAll("path")
            .data(plotData)
          .enter().append("svg:path")
            .attr("d", arc(c,count,prev),plotData)
            .style("fill", colorDict[c])
            .attr("transform", "translate(" + visWidth + "," + visWidth + ")")
          .append("svg:title");
      prev.add(c);
      }
}



function loadData(error,data) {
	if(error) {
		throw error;
	}
	allData = data;
	console.log('Data loaded succesfully!!!');

	//SAVING COLUMN NAMES AND TOTAL NUMBER OF ROWS
	columnNames = Object.keys(data[0]);
	total=0;
	data.forEach(function(d) {
		total += 1;
		/*for(var c=0;c<(columnNames.length-1);c++) { //ITERATING THROUGH ALL (EXCEPT LAST) COLUMNS OF INPUT DATASET
            d[columnNames[c]]=+d[columnNames[c]]; //CONVERT ALL VALUES FROM STRING TO INTEGER
          }*/
      for(var c=0;c<order.length;c++) { //ITERATING THROUGH THE ORDER SUPPLIED BY USER !WARNING
              //console.log(c+' '+order[c]);
              d[columnNames[order[c]]]=+d[columnNames[order[c]]]; //CONVERT ALL VALUES FROM STRING TO INTEGER
              }
	});
	createGiantWheel(allData,columnNames);
}



function chart_wheel(inputParam) {
    console.log('-------chart_wheel----')
	datasetPath=inputParam['dataset'];
	order=inputParam['order'];
	classColumn=inputParam['classColumn'];
	colorDict=inputParam['colorDict'];

	w=inputParam['width'];
	h=inputParam['height'];
	visWidth=w/2;
	r = Math.min(w, h) / 2;
	container=inputParam['container'];
  console.log('gaint-wheel called');
	d3.csv(datasetPath, loadData);

}
