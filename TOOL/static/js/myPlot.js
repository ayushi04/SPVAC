var margin;
var width,height;
var x ;
var y ;
var color = d3.scale.category10();

var xAxis;
var yAxis;
var border=1;
var data;
var classNameCounter;
var intid;
function drawBoundary(svg) {
  var bordercolor="green";
  var borderPath = svg.append("rect")
          .attr("x", 0)
          .attr("y", 0)
          .attr("height", height)
          .attr("width", width)
          .style("stroke", bordercolor)
          .style("fill", "none")
          .style("stroke-width", border);
}

function drawScatterPlot_blob(filepath,svg,className) {
  d3.tsv(filepath, function(error, data) {
    if(error) {
      console.log('Input tsv file path is invalid!! Check filepath once or input file is not a tsv file.');
    }
    data.forEach(function(d) {
      d['0']= +d['0']; //CONVERTING STRING TO NUMERIC VALUE
      d['1']= +d['1']; //CONVERTING STRING TO NUMERIC VALUE
    });
    x.domain(d3.extent(data,function(d) { return d['0']})).nice();
    y.domain(d3.extent(data,function(d) { return d['1']})).nice();
    svg.selectAll("."+className)
       .data(data)
       .enter()
       .append('circle')
       .attr("class", function(d,i) {
         return className+'_'+i.toString();
       })
       .attr("r", 2)
       .attr("cx", function(d) { return x(d['0']); })
       .attr("cy", function(d) { return y(d['1']); })
       .attr('point-id', function(d) {
                //console.log(d);
                return d[0].toString();
            })
       .style("fill", function(d) { return color(d.class); })
       //.style("opacity", 0)  //below 5 lines are for animation
       //.transition()
       //.duration(1000)
       //.delay(function(d,i) {return i * 100;})
       //.style("opacity", 1);

      //DRAWING LEGEND FOR EACH CLASS
      var legend = svg.selectAll(".legend")
                      .data(color.domain())
                      .enter().append("g")
                      .attr("class", "legend")
                      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

      legend.append("rect")
          .attr("x", width - 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);

      legend.append("text")
          .attr("x", width - 24)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d; });
    });
}
function newPlot(cid, data, layout) {
  margin = {top: 20, right: 20, bottom: 30, left: 40};
  var w1=400- margin.left - margin.right;
  var h1=1600- margin.top - margin.bottom;
  var svg = d3.select("#div1")
                .append("svg")
                .attr("id","svg1")
                .attr("width", w1+ margin.left + margin.right )
                .attr("height", h1 + margin.top + margin.bottom)
                .append("svg")
                .attr("border",border)
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  width=w1;
  height=width;
  x= d3.scale.linear().range([0, width]);
  y= d3.scale.linear().range([height, 0]);
  xAxis= d3.svg.axis().scale(x).orient("bottom");
  yAxis = d3.svg.axis().scale(y).orient("left");
  var filepath="./data/iris.tsv"
    drawBoundary(svg);
    drawScatterPlot_blob(filepath,svg,'dot1');

  margin = {top: 400, right: 20, bottom: 30, left: 40};
  width=w1;
  height=width;
  x= d3.scale.linear().range([0, width]);
  y= d3.scale.linear().range([height, 0]);
  xAxis= d3.svg.axis().scale(x).orient("bottom");
  yAxis = d3.svg.axis().scale(y).orient("left");
  var svg = d3.select("#svg1")
                .append("svg")
                .attr("border",border)
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  drawBoundary(svg);
  drawScatterPlot_blob(filepath,svg,'dot2');
  svg = d3.select("#svg1");
  /*var circle = svg.append("line")
               .attr("x1", 50)
               .attr("y1", 50)
               .attr("x2", 500)
               .attr("y2", 500);*/
 svg.append("rect")
         .attr("x", 0)
         .attr("y", 0)
         .attr("height", 1600)
         .attr("width", 400)
         .style("stroke", "green")
         .style("fill", "none")
         .style("stroke-width", border);
svg.append("line")
         .attr("x1", 50)
         .attr("y1", 50)
         .attr("x2", 500)
         .attr("y2", 500)
         .attr("stroke-width", 2)
         .attr("stroke", "black");
};
