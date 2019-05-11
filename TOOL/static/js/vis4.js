var highlighted_idx=0,flag=0;
function chart_vis4(inputParam) {
  rowFile = inputParam['rowFile'];
  colFile = inputParam['colFile'];
  dim = inputParam['dim'];
  //colorDict=inputParam['colorDict'];
  w = inputParam['width'];
  h = inputParam['height'];
  rowcolFile = inputParam['rowColFile']
  //visWidth=w/2;
  //r = Math.min(w, h) / 2;
  container = inputParam['container'];
  drawScatter_vis4(rowcolFile, dim, container)
}

function drawScatter_vis4(rowcolFile, dim, container) {
  hoverInfo = document.getElementById('hoverinfo_vis4');
  d3.csv(rowcolFile, function(error1, file1) {
    file1 = file1.map(function(item, i) {
      item['index'] = i + 1;
      return item;
    });

    function unpack(file1, key) {
      return file1.map(function(row) {
        return row[key];
      });
    }
    var rowCol=unpack(file1, 'id');

    var trace1 = {
      x: unpack(file1, dim[0]),
      y: unpack(file1, dim[1]),
      mode: 'markers',
      type: 'scatter',
      name: 'row points',
      text: unpack(file1, 'id')
    };
    var layout = {
        title: "",
        xaxis: {
          title:dim[0]+' subspace value'
        },
        yaxis: {
           title:dim[1]+' subspace value'
       }
     };
       var myPlot=document.getElementById(container);
       var data = [trace1];
     Plotly.newPlot(container, data, layout);
     myPlot.on('plotly_click', function(data){
         var xaxis = data.points[0].xaxis,
             yaxis = data.points[0].yaxis;
         var index=data.points[0].pointIndex;
         var infotext = data.points.map(function(d){
           return ('row: '+d.x+', col: '+d.y+' point: '+rowCol[index]);
         });
         if(flag==1) {
           $('#row_'+col[highlighted_idx]).css({"background-color": "white", "font-size": "100%"});
           $('#col_'+row[highlighted_idx]).css({"background-color": "white", "font-size": "100%"});
         }
         $('#row_'+rowCol[index]).css({"background-color": "yellow", "font-size": "200%"});
         $('#col_'+rowCol[index]).css({"background-color": "yellow", "font-size": "200%"});
         highlighted_idx=index;
         flag=1;
         hoverInfo.innerHTML = infotext.join('');
     });

  });
};
