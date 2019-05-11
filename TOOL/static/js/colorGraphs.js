function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getJaccardPoints() {
  console.log(this, $(this).attr('id'));
  console.log('hello');
  var x = $(this).attr('id').split('_');
  $.ajax({
    url: "/getJaccardPoints",
    data: {
      rowBlock: x[0],
      colBlock: x[1],
      type: x[2], //rowPoints or colPoints
      color1: x[3],
      color2: x[4],
      datasetPath: getParameterByName('datasetName')
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      result = JSON.parse(result);
      A = JSON.parse(result['A_min_B']);
      B = JSON.parse(result['A_int_B']);
      C = JSON.parse(result['B_min_C']);
      htmlstr = convertJsonToTableSet(A, 'A-B');
      $('#jaccardPointsTable1').html(htmlstr); //$('#table2').html(mat[k]);
      $('#jaccardPointsTable2').html(convertJsonToTableSet(B, 'A intersection B'));
      $('#jaccardPointsTable3').html(convertJsonToTableSet(C, 'B-A'));
    }
  });
}

function convertJsonToTable(data, type) {
  var tr;
  htmlstr2 = "<table border='1' ><caption>" + type + "</caption>";
  var i = 0;
  htmlstr2 = htmlstr2.concat("<tr><th bgcolor=#ffffff>&nbsp;&nbsp;&nbsp;</th>")
  data = JSON.parse(data);
  for (key in data[0]) {
    htmlstr2 = htmlstr2.concat("<th  bgcolor=" + key + ">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "</th>")
  }
  htmlstr2 = htmlstr2.concat("</tr>")
  for (var i = 0; i < data.length; i++) {
    htmlstr2 = htmlstr2.concat('<tr><td bgcolor=' + Object.keys(data[0])[i] + '>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>');
    for (key in data[i]) {
      //if(key=='id')
      htmlstr2 = htmlstr2.concat("<td id='" + type + '_' + Object.keys(data[0])[i] + '_' + key + "' >" + data[i][key] + "</td>");
      //else
      //htmlstr2 = htmlstr2.concat("<td>" + data[i][key] + "</td>");
      //htmlstr2 = htmlstr2.concat("<td>" + data[i].b + "</td>");
      //htmlstr2 = htmlstr2.concat("<td>" + data[i].c + "</td>");
      //htmlstr2 = htmlstr2.concat("<td>" + data[i].d + "</td>");
    }
    htmlstr2 = htmlstr2.concat('</tr>');
  }
  htmlstr2 = htmlstr2.concat('</table>');
  return htmlstr2;
}

function convertJsonToTableSet(data, type) {
  var tr;
  htmlstr2 = "<table border='1'>";
  var i = 0;
  htmlstr2 = htmlstr2.concat("<tr>")
  for (key in data[0]) {
    htmlstr2 = htmlstr2.concat("<th>" + key + "</th>")
  }
  htmlstr2 = htmlstr2.concat("</tr>")
  for (var i = 0; i < data.length; i++) {
    htmlstr2 = htmlstr2.concat('<tr>');
    for (key in data[i]) {
      if (key == 'id')
        htmlstr2 = htmlstr2.concat("<td id='" + data[i][key] + "' onclick='hoverall(this)'>" + data[i][key] + "</td>");
      else
        htmlstr2 = htmlstr2.concat("<td>" + data[i][key] + "</td>");
    }
    htmlstr2 = htmlstr2.concat('</tr>');
  }
  htmlstr2 = htmlstr2.concat('</table>');
  return htmlstr2;
}

function hoverall(x) {
  console.log(x, $(x).attr('id'));

  //Plotly.Fx.hover('0_1_#db41e20', [{curveNumber: 0, pointNumber: 0}],
}

function redrawIdPlot(key, rowPoints, colPoints, subspace, myid, pointsId) {
  //var allDiv=$("div[id^='"+key+"']");
  rowPoints = JSON.parse(rowPoints);
  colPoints = JSON.parse(colPoints);
  var rowId = rowPoints.map(a => a.id);
  var colId = colPoints.map(a => a.id);
  if (typeof(subspace[0]) === 'string')
    subspace = [subspace];
  for (var i = 0; i < subspace.length; i++) {
    cid = key + i;
    if (subspace[i].length == 1) {
      var cl = [];
      var defcolor = key.split('_')[2];
      for (var j = 0; j < rowPoints.length; j++) {
        if (pointsId.includes(rowPoints[j]['id']))
          cl.push(defcolor);
        else
          cl.push('#E8E8E8');
      }
      var data_update = {
        marker: {
          color: cl
        }
      };
      var layout_update = {
        //title: 'some new title', // updates the title
      };
      Plotly.update(cid, data_update, layout_update);
    } //if subspace[i]
    if (subspace[i].length == 2) {
      var cl = [];
      var defcolor = "blue";
      for (var j = 0; j < rowPoints.length; j++) {
        if (pointsId.includes(rowPoints[j]['id']))
          cl.push(defcolor);
        else
          cl.push('#E8E8E8'); //LIGHT-GREY COLOR
      }
      var data_update = {
        marker: {
          color: cl
        }
      };
      var layout_update = {
        //title: 'some new title', // updates the title
      };
      Plotly.update(cid, data_update, layout_update, [0]);

      cl = [];
      defcolor = "orange";
      for (var j = 0; j < colPoints.length; j++) {
        if (pointsId.includes(colPoints[j]['id']))
          cl.push(defcolor);
        else
          cl.push('#E8E8E8'); //LIGHT-GREY COLOR
      }
      var data_update = {
        marker: {
          color: cl
        }
      };
      var layout_update = {
        //title: 'some new title', // updates the title
      };
      Plotly.update(cid, data_update, layout_update, [1]);

    } //if subspace len==2
  } //for

} //fn

function draw1dPlot(containerid, rowPoints, colPoints, subspace) {
  rowPoints = JSON.parse(y[key]['rowPoints']);
  colPoints = JSON.parse(y[key]['colPoints']);
  console.log(containerid, rowPoints, colPoints);
  var rowId = rowPoints.map(a => a.id);
  var colId = colPoints.map(a => a.id);
  var text = rowId.map(function(num, idx) {
    return num + "," + colId[idx];
  });
  if (typeof(subspace[0]) === 'string')
    subspace = [subspace];
  for (var i = 0; i < subspace.length; i++) {
    cid = containerid + i;
    $('#allPlots').append("<div id='" + cid + "' class='cover-item' subspace='" + subspace[i].toString() + "'></div>");
    if (subspace[i].length == 1) {
      var trace1 = {
        y: rowPoints.map(a => a[subspace[i]]),
        x: colPoints.map(a => a[subspace[i]]),
        mode: 'markers',
        type: 'scatter',
        name: 'row points',
        text: text,
        class: text,
        cid: cid,
        marker: {
          //size : 10,
          color: containerid.split('_')[2]
        }
        //text : document.getElementById('hoverinfo')
      };
      var layout = {
        title: "Row Block : " + containerid.split('_')[0] + " Column Block : " + containerid.split('_')[1],
        width: 500,
        height: 500,
        xaxis: {
          title: '<b>' + subspace[i] + '</b>'
        },
        yaxis: {
          title: '<b>' + subspace[i] + '</b>'
        },
        dragmode: 'lasso'
        //paper_bgcolor:containerid.split('_')[2]
      };
      var myPlot = document.getElementById(containerid);
      var data = [trace1];
      Plotly.newPlot(cid, data, layout);
      var myPlot = document.getElementById(cid);
      myPlot.on('plotly_selected', function(data) {
        var points = data.points;
        var pointsId = [],
          rowPointsId = [],
          colPointsId = [];
        for (var i = 0; i < points.length; i++) {
          var t;
          t = points[i].text.split(',');
          pointsId.push(t[0]);
          pointsId.push(t[1]);
          rowPointsId.push(t[0]);
          colPointsId.push(t[1]);
        }
        //FILTER POINT FROM SORTED DATA
        //DISPLAY POINTS
        //OVERWRITE COLOR FOR NON-EXISTANT PLOTS
        //RESTYLE OTHER GRAPHS (IMP) DO FIRST
        updateOtherGraphs(pointsId, cid);
        displaySelectedPoints(rowPointsId, colPointsId);
      });

      myPlot.on('plotly_click', function(data) {
        var xaxis = data.points[0].xaxis,
          yaxis = data.points[0].yaxis;
        var infotext = data.points.map(function(d) {
          return ('row: ' + d.x + ', col: ' + d.y);
        });
        var index = data.points[0].text;
        index = index.split(',');

        if ($('#' + index[0]).length) {
          $('#' + index[0]).css({
            "background-color": "yellow",
            "font-size": "200%"
          });
          var topPos = document.getElementById(index[0]).offsetTop;
          var parent = $('#' + index[0]).closest('div').attr('id');
          document.getElementById(parent).scrollTop = topPos - 10;
        }
        if ($('#' + index[1]).length) {
          $('#' + index[1]).css({
            "background-color": "yellow",
            "font-size": "200%"
          });
          var topPos = document.getElementById(index[1]).offsetTop;
          var parent = $('#' + index[1]).closest('div').attr('id');
          document.getElementById(parent).scrollTop = topPos - 10;
        }
      });
    } else if (subspace[i].length == 2) {
      var trace1 = {
        y: rowPoints.map(a => a[subspace[i][0]]),
        x: rowPoints.map(a => a[subspace[i][1]]),
        mode: 'markers',
        type: 'scatter',
        name: 'row points',
        text: rowId,
        class: text,
        marker: {
          //size : 10,
          color: "blue"

        }
        //text : document.getElementById('hoverinfo')
      };
      var trace2 = {
        y: colPoints.map(a => a[subspace[i][0]]),
        x: colPoints.map(a => a[subspace[i][1]]),
        mode: 'markers',
        type: 'scatter',
        name: 'col points',
        text: colId,
        marker: {
          //size : 10,
          color: "orange"

        }
      };
      var layout = {
        title: "Row Block : " + containerid.split('_')[0] + " Column Block : " + containerid.split('_')[1],
        width: 500,
        height: 500,
        xaxis: {
          title: '<b>' + subspace[i][1] + '</b>'
        },
        yaxis: {
          title: '<b>' + subspace[i][0] + '</b>'
        },
        dragmode: 'lasso'
        //paper_bgcolor:containerid.split('_')[2]
      };
      var myPlot = document.getElementById(containerid);
      var data = [trace1, trace2];
      Plotly.newPlot(cid, data, layout);
      var myPlot = document.getElementById(cid);
      myPlot.on('plotly_selected', function(data) {
        var points = data.points;
        var pointsId = [],
          rowPointsId = [],
          colPointsId = [];
        for (var i = 0; i < points.length; i++) {
          var t;
          t = points[i].text;
          pointsId.push(t);
          if (points[i].curveNumber == 0)
            rowPointsId.push(t);
          else colPointsId.push(t);
        }
        //FILTER POINT FROM SORTED DATA
        //DISPLAY POINTS
        //OVERWRITE COLOR FOR NON-EXISTANT PLOTS
        //RESTYLE OTHER GRAPHS (IMP) DO FIRST
        updateOtherGraphs(pointsId, cid);
        displaySelectedPoints(rowPointsId, colPointsId);
      });

    } else if (subspace[i].length == 3) {
      //DRAW 3-D SCATTER
      var trace1 = {
        y: rowPoints.map(a => a[subspace[i][0]]),
        x: rowPoints.map(a => a[subspace[i][1]]),
        z: rowPoints.map(a => a[subspace[i][2]]),
        mode: 'markers',
        type: 'scatter',
        name: 'row points',
        text: rowId,
        class: text,
        marker: {
          //size : 10,
        },
        type: 'scatter3d'
        //text : document.getElementById('hoverinfo')
      };
      var trace2 = {
        y: colPoints.map(a => a[subspace[i][0]]),
        x: colPoints.map(a => a[subspace[i][1]]),
        z: rowPoints.map(a => a[subspace[i][2]]),
        mode: 'markers',
        type: 'scatter',
        name: 'column points',
        text: colId,
        marker: {
          //size : 10,
        },
        type: 'scatter3d'
      };

      var layout = {
        scene: {
          xaxis: {
            title: subspace[i][0]
          },
          yaxis: {
            title: subspace[i][1]
          },
          zaxis: {
            title: subspace[i][2]
          },
        },
        autosize: false,
        width: 550,
        height: 500,
        dragmode: 'lasso'
      };
      var myPlot = document.getElementById(containerid);
      var data = [trace1, trace2];
      Plotly.newPlot(cid, data, layout);
      var myPlot = document.getElementById(cid);
      myPlot.on('plotly_selected', function(data) {
        var points = data.points;
        var pointsId = [],
          rowPointsId = [],
          colPointsId = [];
        for (var i = 0; i < points.length; i++) {
          var t;
          t = points[i].text.split(',');
          pointsId.push(t[0]);
          if (points[i].curveNumber == 0)
            rowPointsId.push(t);
          else colPointsId.push(t);
        }
        //FILTER POINT FROM SORTED DATA
        //DISPLAY POINTS
        //OVERWRITE COLOR FOR NON-EXISTANT PLOTS
        //RESTYLE OTHER GRAPHS (IMP) DO FIRST
        updateOtherGraphs(pointsId, cid);
        displaySelectedPoints(rowPointsId, colPointsId);
      });
    }
  }
} //fn

function updateOtherGraphs(pointsId, myid) {
  //GET ALL ID OF PLOTS AS A LIST
  allId = getAllId();
  console.log('allIds are %s', allId.toString());
  for (var i = 0; i < allId.length; i++) {
    var key = allId[i];
    var rp = y[key]['rowPoints'];
    var cp = y[key]['colPoints'];
    var subspaceList = y[key]['subspace'];
    //rowPoints=rp;
    //colPoints=cp;
    //subspace=subspaceList;
    redrawIdPlot(key, rp, cp, subspaceList, myid, pointsId);

    var p1 = document.getElementById(allId[i]);

  } //for
} //fn

function displaySelectedPoints(rowPointsId, colPointId) {
  var t = 1;
  var rowPoints = $(allData)
    .filter(function(i, n) {
      return rowPointsId.includes(n.id);
    });
  var colPoints = $(allData)
    .filter(function(i, n) {
      return colPointId.includes(n.id);
    });
  //selectedPoints
  $('#selectedPoints_row').html(convertJsonToTableSet(colPoints, 'col'));
  $('#selectedPoints_col').html(convertJsonToTableSet(rowPoints, 'row'));
  drawInteractiveScatter('#scatterPlotLegend', 'scatterPlot', rowPoints, colPoints);

}
var inter_rp,inter_cp,allDims;
function drawInteractiveScatter(divid, scatterid, rowPoints, colPoints) {
  var rowP = [],
    colP = [];
  for (var i = 0; i < rowPoints.length; i++) {
    rowP.push(rowPoints[i]);
  }
  for (var i = 0; i < colPoints.length; i++) {
    colP.push(colPoints[i]);
  }
  rowPoints = rowP;
  colPoints = colP;
  inter_rp=rowPoints;
  inter_cp=colPoints;
  var rowId = rowPoints.map(a => a.id);
  var colId = colPoints.map(a => a.id);
  var text = rowId.map(function(num, idx) {
    return num + "," + colId[idx];
  });
  allDims = Object.keys(rowPoints[0]); //["id", "var_WTI", "skewness_WTI", "curtosis_WTI", "entropy_image", "classLabel"]
  var htmlstr2 = '';
  htmlstr2 = htmlstr2.concat('<select id="filterx">');
  for (var i = 0; i < allDims.length; i++) {
    var k = allDims[i];
    if (k != 'classLabel' && k != 'id') {
      //htmlstr2 = htmlstr2.concat('<option value="' + k + '" name="filterCol" class="filterCol" >' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
      htmlstr2 = htmlstr2.concat('<option value="' + k + '">' + k + '</option>');
    }
  }
  htmlstr2 = htmlstr2.concat('</select>');
  $(divid).append("<div id='xaxis' ></div>");
  $('#xaxis').html(htmlstr2);

  var htmlstr2 = '';
  htmlstr2 = htmlstr2.concat('<select id="filtery">');
  for (var i = 0; i < allDims.length; i++) {
    var k = allDims[i];
    if (k != 'classLabel' && k != 'id') {
      //htmlstr2 = htmlstr2.concat('<option value="' + k + '" name="filterCol" class="filterCol" >' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
      htmlstr2 = htmlstr2.concat('<option value="' + k + '">' + k + '</option>');
    }
  }
  htmlstr2 = htmlstr2.concat('</select><button id="go">GO</button>');

  $(divid).append("<div id='yaxis' ></div>");
  $('#yaxis').html(htmlstr2);

}

function updateInteractiveScatter() {
  xaxis=$("#filterx").val();
  yaxis=$("#filtery").val();

  var rowPoints=inter_rp;
  var colPoints=inter_cp;
  var rowId = rowPoints.map(a => a.id);
  var colId = colPoints.map(a => a.id);
  var data1=[];
    var trace1 = {
        y: rowPoints.map(a => a[xaxis]),
        x: rowPoints.map(a => a[yaxis]),
        z: rowPoints.map( (a,i)=> 0),
        mode: 'markers',
        name: 'row points',
        text: rowId,
        marker : {
                size : 2,
                //size : 10,
                color:"blue"
              },
        visible: true,
        type: 'scatter3d'
        //text : document.getElementById('hoverinfo')
      };
      var trace2 = {
          y: colPoints.map(a => a[xaxis]),
          x: colPoints.map(a => a[yaxis]),
          z: colPoints.map( (a,i)=> 0),
          mode: 'markers',
          name: 'column points',
          text: colId,
          marker : {
                  size : 2,
                  //size : 10,
                  color:"orange"
                },
          visible: true,
          type: 'scatter3d'
        };
        data1.push(trace1);
        data1.push(trace2);
        var lists=[],temp=new Array(allDims.length*2-2).fill(false);
        temp[0]=true;
        temp[1]=true;
        lists.push([temp.slice()]);
        temp[0]=false;
        temp[1]=false;
        var t=2;
        for (var i = 0; i < allDims.length; i++) {
          var k = allDims[i];
          if (k != 'classLabel' && k != 'id') {
            var trace3 = {
                y: rowPoints.map(a => a[xaxis]),
                x: rowPoints.map(a => a[yaxis]),
                z: rowPoints.map(a => a[k]),
                mode: 'markers',
                name: 'row points',
                text: rowId,
                marker : {
                        //size : 10,
                        size : 2,
                        color:"blue"
                      },
                visible: false,
                type: 'scatter3d'
                //text : document.getElementById('hoverinfo')
              };
              var trace4 = {
                  y: colPoints.map(a => a[xaxis]),
                  x: colPoints.map(a => a[yaxis]),
                  z: rowPoints.map(a => a[k]),
                  mode: 'markers',
                  name:'column points',
                  text: colId,
                  marker : {
                          size : 2,
                          color:"orange"
                        },
                  visible: false,
                  type: 'scatter3d'
                };
              data1.push(trace3);
              data1.push(trace4);
          }
          temp[t]=true;
          temp[t+1]=true;
          lists.push([temp.slice()]);
          temp[t]=false;
          temp[t+1]=false;
          t=t+2;
        }
    console.log(data1.length);
    var layout = {
                      scene: {
                        xaxis:{title: xaxis},
                        yaxis:{title: yaxis},
                        zaxis:{title: 'z'},
                        },
                      autosize: false,
                      width: 550,
                      height: 500,
                      updatemenus: [{
                              y: 1,
                              yanchor: 'top',
                              buttons: [{
                                  method: 'restyle',
                                  args: ['visible', [true,true,false,false,false,false,false,false,false,false]],
                                  label: 'None'
                              },{
                                  method: 'restyle',
                                  args: ['visible', [false,false,true,true,false,false,false,false,false,false]],
                                  label: allDims[1]
                              }, {
                                  method: 'restyle',
                                  args: ['visible', [false,false,false,false,true,true,false,false,false,false]],
                                  label:allDims[2]
                              }, {
                                  method: 'restyle',
                                  args: ['visible', [false,false,false,false,false,false,true,true,false,false]],
                                  label: allDims[3]
                              }, {
                                  method: 'restyle',
                                  args: ['visible', [false,false,false,false,false,false,false,false,true,true]],
                                  label: allDims[4]
                              }]
                          }],
                    };
    Plotly.newPlot('scatterPlot', data1, layout);


}

function getAllId() {
  var allId = [];
  for (key in y) {
    allId.push(key);
  }
  return allId;
}
