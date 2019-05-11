var highlighted_idx=0,flag=0;
function chart_vis3(inputParam) {
  rowFile = inputParam['rowFile'];
  colFile = inputParam['colFile'];
  dim = inputParam['dim'];
  //colorDict=inputParam['colorDict'];
  w = inputParam['width'];
  h = inputParam['height'];
  //visWidth=w/2;
  //r = Math.min(w, h) / 2;
  container = inputParam['container'];
  drawScatter_vis3(rowFile,colFile,dim,container)
}

function drawScatter_vis3(rowFile,colFile,dim,container) {
  hoverInfo = document.getElementById('hoverinfo');
  d3.csv(rowFile, function(error1, file1) {
  d3.csv(colFile, function(error2, file2) {
    file1 = file1.map(function(item, i) {
      item['index'] = i + 1;
      return item;
    });
    file2 = file2.map(function(item, i) {
      item['index'] = i + 1;
      return item;
    });
      function unpack(file1, key) {
        return file1.map(function(row) {
          return row[key];
        });
      }
      var text=[];
      var row=unpack(file1, 'id'),col=unpack(file2, 'id');
      for (var i=0;i<row.length;i++)
        text.push(row[i]+','+col[i]);

      var trace1 = {
          y: unpack(file1, dim),
          x: unpack(file2, dim),
          mode: 'markers',
          type: 'scatter',
          name: 'row points',
          text: unpack(file2,dim),
          type: 'scatter3d'
          //text : document.getElementById('hoverinfo')
        };
        var layout = {
            title: "",
            xaxis: {
              title:dim+' subspace value'
           },
           yaxis: {
              title:dim+' subspace value'
          }
        };
      //Plotly.plot(TESTER, container, layout);
      var myPlot=document.getElementById(container);
      var data = [trace1];
      Plotly.newPlot(container, data, layout);
      myPlot.on('plotly_click', function(data){
          var xaxis = data.points[0].xaxis,
              yaxis = data.points[0].yaxis;
          var infotext = data.points.map(function(d){
            return ('row: '+d.x+', col: '+d.y);
          });
          var index=data.points[0].pointIndex;
          console.log(file1[index+4])
          console.log(file2[index+4]);
          console.log(data);
          console.log(file1);
          console.log(file2);
          console.log(row[index]+','+col[index])
          if(flag==1) {
            $('#row_'+col[highlighted_idx]).css({"background-color": "white", "font-size": "100%"});
            $('#col_'+row[highlighted_idx]).css({"background-color": "white", "font-size": "100%"});
          }
          $('#row_'+col[index]).css({"background-color": "yellow", "font-size": "200%"});
          $('#col_'+row[index]).css({"background-color": "yellow", "font-size": "200%"});
          highlighted_idx=index;
          flag=1;
          hoverInfo.innerHTML = infotext.join('');
      })
       /*.on('plotly_unhover', function(data){
          hoverInfo.innerHTML = '';
          $('#row_'+col[index]).css({"background-color": "white", "font-size": "100%"});
          $('#col_'+row[index]).css({"background-color": "white", "font-size": "100%"});

      });*/

    });
  });
}
