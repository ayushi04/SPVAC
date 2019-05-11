var filterList = new Set();
var highlighted_idx=0,flag=0;
var colNames;
function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function dynamicallyLoadSelectList_closed(divId,divId1,divId2) {
  d3.csv(getParameterByName('datasetPath'), function(error, csv) {
      colNames = d3.values(csv)[0];
      //FETCHING FILTERING COLUMN UNIQUE VALUES
      var map1 = {};
      csv.forEach(function(d) {
        for (c in colNames) {
          if (c.indexOf("filter") >= 0) {
            filterList.add(c);
            if (!(c in map1)) {
              map1[c] = new Set();
              map1[c].add(d[c]);
            } else map1[c].add(d[c]);
          }
        }
      });

      var filterstr = "";
      for (k in map1) {
        filterstr = filterstr.concat('<select id="' + k + '">');
        console.log(filterstr);
        map1[k].forEach(function(d) {
          filterstr = filterstr.concat('<option value="' + d + '">' + d + '</option>');
        });
        filterstr = filterstr.concat('</select>&nbsp;&nbsp;');
      }
      $(divId).html(filterstr);
      //dynamicallyLoadSelectListHelper(divId1,divId2);
      var htmlstr = '',
        htmlstr2 = '';
      var i = 0;
      for (k in colNames) {
        if (k != 'classLabel' && k != 'id') {
          htmlstr = htmlstr.concat('<input type="checkbox" class="dim" value="' + i + '">' + k + '<br>');
          //htmlstr2 = htmlstr2.concat('<input type="radio" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;')
          i++;
          htmlstr2 = htmlstr2.concat('<input type="checkbox" value="' + i + '" name="order_dim" class="order_dim">' + i + '-d</input>&nbsp;&nbsp;&nbsp;&nbsp;');
        }
      }
      $(divId1).html(htmlstr);
      $(divId2).html(htmlstr2);
    });
}

function dynamicallyLoadSelectList(divId,divId1,divId2) { //eg., #filterlist
  d3.csv(getParameterByName('datasetPath'), function(error, csv) {
      colNames = d3.values(csv)[0];
      //FETCHING FILTERING COLUMN UNIQUE VALUES
      var map1 = {};
      csv.forEach(function(d) {
        for (c in colNames) {
          if (c.indexOf("filter") >= 0) {
            filterList.add(c);
            if (!(c in map1)) {
              map1[c] = new Set();
              map1[c].add(d[c]);
            } else map1[c].add(d[c]);
          }
        }
      });

      var filterstr = "";
      for (k in map1) {
        filterstr = filterstr.concat('<select id="' + k + '">');
        console.log(filterstr);
        map1[k].forEach(function(d) {
          filterstr = filterstr.concat('<option value="' + d + '">' + d + '</option>');
        });
        filterstr = filterstr.concat('</select>&nbsp;&nbsp;');
      }
      $(divId).html(filterstr);
      dynamicallyLoadSelectListHelper(divId1,divId2);
    });
  }

function dynamicallyLoadSelectListHelper(divId1, divId2) {
    var htmlstr = '',
      htmlstr2 = '';
    var i = 0;
    for (k in colNames) {
      if (k != 'classLabel' && k != 'id') {
        htmlstr = htmlstr.concat('<input type="checkbox" class="dim" value="' + k + '">' + k + '<br>');
        //htmlstr2 = htmlstr2.concat('<input type="radio" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;')
        htmlstr2 = htmlstr2.concat('<input type="checkbox" value="' + k + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
        i++;
      }
    }
    $(divId1).html(htmlstr);
    $(divId2).html(htmlstr2);
  }

function colorFilter(m1,m2,p1,p2,color_val,imgType) {
  //console.log(this, $(this).attr('bgcolor'));
  console.log('hello');
  //var imgType='_'+ $('#changeImgType').val();
  var grid = $("input[name=grid]:checked").val();
  $('#loading').html('<img src="static/image/loading.gif"> loading...');
  $.ajax({
    url: "/redrawimg",
    data: {
      color_value: color_val,
      datasetPath: getParameterByName('datasetPath'),
      imgType: '_'+imgType,
      grid:grid
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      //$("#div1").html("<img src='static/output/img_bea.png'></img>");
      console.log(result);
      $('#'+m1).remove();
      $('#'+p1).append('<div id="'+m1+'" style="width: 500px; height: 400px;"></div>')
      $('#'+m2).remove();
      $('#'+p2).append('<div id="'+m2+'" style="width: 500px; height: 400px;"></div>')
      d = new Date();
      if(imgType=='heidi')
        loadImg("/static/output/temp_heidi.png?" + d.getTime(),"/static/output/temp_heidi_composite.png?" + d.getTime(), 2229, 2058,m1,m2,p1,p2,imgType);
      else
        loadImg("/static/output/temp_closed.png?" + d.getTime(),"/static/output/temp_closed_composite.png?" + d.getTime(), 2229, 2058,m1,m2,p1,p2,imgType);
      $('#loading').html('-');
    }
  });
}

function updateImage() {
  console.log('--updateImage called--');
  var dimList = [];
  //var imgType =  '_'+$('#changeImgType').val();
  $(".dim:checked").each(function() {
    dimList.push($(this).val());
  });
  dimList = dimList.join(' ');
  var orderDim = [];
  $(".order_dim:checked").each(function() {
    orderDim.push($(this).val());
  });
  orderDim = orderDim.join(' ');

  //var orderDim = $(".order_dim:checked").val();
  var grid = $("input[name=grid]:checked").val();
  var filterDict = {};
  console.log(dimList, orderDim, filterList, grid);
  $('#loading').html('<img src="loading.gif"> loading...');
  filterList.forEach(function(d) {
    filterDict[d] = $('#' + d).val();
  });
  console.log(filterDict);
  $('.alert_msg').css("display", "none");
  $.ajax({
    url: "/image",
    data: {
      order_dim: orderDim,
      selectedDim: dimList,
      filterDict: JSON.stringify(filterDict),
      datasetPath: getParameterByName('datasetPath'),
      grid: grid,
      imgType: 'heidi',//$('#changeImgType').val() //NO NEED, LEFT IT JUST TO KEEP THE CODE CONTINUE RUNNING
      knn:$("#knn").val()
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      console.log(result);
      var result1=JSON.parse(result);
      if(result1.hasOwnProperty('error')) {
        var message=result1['error'];
        $('.error_msg').html(message);
        $('.alert_msg').css("display", "inline-block");
      }
      else{
        var subspace=result1['subspace'];
        var output=result1['output'];
        var subspaceList="";
        for(var i=0;i<subspace.length;i++) {
          subspaceList = subspaceList.concat('<input type="checkbox" class="subspace" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
        }
        $('#subspace').html(subspaceList);
        $('#mapid').remove();
        $('#mapid2').remove();
        $('#mapid3').remove();
        $('#mapid4').remove();
        $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
        $('#parent2').append('<div id="mapid2" style="width: 500px; height: 400px;"></div>')
        $('#parent3').append('<div id="mapid3" style="width: 500px; height: 400px;"></div>')
        $('#parent4').append('<div id="mapid4" style="width: 500px; height: 400px;"></div>')
        d = new Date();
        loadImg("/static/output/consolidated_img.png?" + d.getTime(),"/static/output/consolidated_composite.png?" + d.getTime(), 2229, 2058,'mapid','mapid2','parent','parent2','heidi');
        loadImg("/static/output/closed_img.png?" + d.getTime(),"/static/output/closed_composite.png?" + d.getTime(), 2229, 2058,'mapid3','mapid4','parent3','parent4','closed');
        $('#loading').html('-');
        var fname = '/static/output/legend_heidi.html?' + d.getTime();
        $('#legend').load(fname);
        var fname = '/static/output/legend_closed.html?' + d.getTime();
        $('#legend2').load(fname);
        //$('#legend').load("{{ url_for('static',filename='fname') }}".replace('fname', fname));
      }
    },
     error: function(error) {
                console.log('ERROR',error);
            } 
  });
}
function uploadTree() {
  console.log('--uploadTree --');
  var dimList = [];
  $(".dim:checked").each(function() {
    dimList.push($(this).val());
  });
  dimList = dimList.join(' ');
  var orderDim = [];
  $(".order_dim:checked").each(function() {
    orderDim.push($(this).val());
  });
  orderDim = orderDim.join(' ');

  var grid = $("input[name=grid]:checked").val();
  var filterDict = {};
  console.log(dimList, orderDim, filterList, grid);
  filterList.forEach(function(d) {
    filterDict[d] = $('#' + d).val();
  });
  console.log(filterDict);
  $.ajax({
    url: "/subspace_all",
    data: {
      order_dim: orderDim,
      selectedDim: dimList,
      filterDict: JSON.stringify(filterDict),
      datasetPath: getParameterByName('datasetPath'),
      grid: grid,
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      console.log(result);
      //$("html").empty();
      $("html").append(result);
    },
     error: function(error) {
                console.log('ERROR',error);
            } 
  });

}


function resetImage() {
  console.log('--reset image --');
  //console.log($('#changeImgType').val());
  //var imgType='_'+$('#changeImgType').val();
  $('#loading').html('<img src="loading.gif"> loading...');
  var grid = $("input[name=grid]:checked").val();
  $.ajax({
    url: "/resetImage",
    data: {
      datasetPath: getParameterByName('datasetPath'),
      grid: grid,
      imgType: 'heidi' //$('#changeImgType').val()  //NEED TO WORK ON THIS LATER, GET ACTIVE TAB
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      var result1=JSON.parse(result);
      //console.log(result+result1);
      var subspace=result1['subspace'];
      var output=result1['output'];
      var subspaceList='<form action="\/dashboard" method="get" target="_blank">';
      subspaceList = subspaceList.concat('<input type="hidden" name="datasetName" value="'+getParameterByName('datasetPath')+'">');
      for(var i=0;i<subspace.length;i++) {
        subspaceList = subspaceList.concat('<input type="checkbox" class="subspace" value="' + subspace[i].toString() + '" name="subspace" class="order_dim">' + subspace[i].toString() + '</input>&nbsp;&nbsp;&nbsp;&nbsp;<br/>');
      }
      subspaceList = subspaceList.concat('<input type="submit" value="Submit"></form>');
      $('#mapid').remove();
      $('#mapid2').remove();
      $('#mapid3').remove();
      $('#mapid4').remove();
      $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
      $('#parent2').append('<div id="mapid2" style="width: 500px; height: 400px;"></div>')
      $('#parent3').append('<div id="mapid3" style="width: 500px; height: 400px;"></div>')
      $('#parent4').append('<div id="mapid4" style="width: 500px; height: 400px;"></div>')
      d = new Date();
      loadImg("/static/output/consolidated_img.png?" + d.getTime(),"/static/output/consolidated_composite.png?" + d.getTime(), 2229, 2058,'mapid','mapid2','parent','parent2','heidi');
      loadImg("/static/output/closed_img.png?" + d.getTime(),"/static/output/closed_composite.png?" + d.getTime(), 2229, 2058,'mapid3','mapid4','parent3','parent4','closed');
      $('#loading').html('-');
      var fname = '/static/output/legend_heidi.html?' + d.getTime();
      $.get(fname,function(d) {
        var d1='<form action="/dashboard2" method="get" target="_blank"> <div>Blockwise? <input type="radio" value="yes" name="blockwise">yes<input type="radio" value="no" name="blockwise">no</div> <input type="hidden" name="datasetName" value="'+getParameterByName('datasetPath')+'"> <input type="hidden" name="imgType" value="heidi">'+d+'<input type="submit" value="Submit"></form>';
        $('#legend').html(d1);
      },'html');
      console.log('legend loaded succesfully');
      var fname = '/static/output/legend_closed.html?' + d.getTime();
      $.get(fname,function(d) {
        var d1='<form action="/dashboard2" method="get" target="_blank"> <div>Blockwise? <input type="radio" value="yes" name="blockwise">yes<input type="radio" value="no" name="blockwise">no</div> <input type="hidden" name="datasetName" value="'+getParameterByName('datasetPath')+'"> <input type="hidden" name="imgType" value="closed">'+d+'<input type="submit" value="Submit"></form>';
        $('#legend2').html(d1);
      },'html');
      
    }
  });

}

function loadImg(url,url2, w, h,mapid,mapid2,parent,parent2,imgType) {
  var MIN_ZOOM = -1;
  var MAX_ZOOM = 5;
  var INITIAL_ZOOM = 1;
  var ACTUAL_SIZE_ZOOM = 3;
  var map = L.map(mapid, {
    minZoom: MIN_ZOOM,
    maxZoom: MAX_ZOOM,
    center: [0, 0],
    zoom: INITIAL_ZOOM,
    crs: L.CRS.Simple
  });
  //var imgType='_'+ $('#changeImgType').val();


  var southWest = map.unproject([0, h], ACTUAL_SIZE_ZOOM);
  var northEast = map.unproject([w, 0], ACTUAL_SIZE_ZOOM);
  console.log(southWest, northEast);
  var bounds = new L.LatLngBounds(southWest, northEast);

  L.imageOverlay(url, bounds).addTo(map);



  map.setMaxBounds(bounds);

  var map2 = L.map(mapid2, {
    minZoom: MIN_ZOOM,
    maxZoom: MAX_ZOOM,
    center: [0, 0],
    zoom: INITIAL_ZOOM,
    crs: L.CRS.Simple
  });
  
  //var southWest = map2.unproject([0, h], ACTUAL_SIZE_ZOOM);
  //var northEast = map2.unproject([w, 0], ACTUAL_SIZE_ZOOM);
  //console.log(southWest, northEast);
  //var bounds = new L.LatLngBounds(southWest, northEast);

  L.imageOverlay(url2, bounds).addTo(map2);
  map2.setMaxBounds(bounds);


  map.on('click', function(e) {
    var x = (e.latlng.lat) / (southWest.lat - northEast.lat);
    var y = (e.latlng.lng) / (-southWest.lng + northEast.lng);
    console.log(x + ':' + y);
    var gridPatterns = $("input[name=ptype]:checked").val();
    var grid = $("input[name=grid]:checked").val();
    console.log(gridPatterns+' '+grid);
    $('#loading').html('<img src="loading.gif"> loading...');
    $('#table2').html('-');
    $('#table3').html('-');

    $.ajax({
      url: "/highlightPattern",
      data: {
        x: x,
        y: y,
        datasetPath: getParameterByName('datasetPath'),
        imgType: imgType,//$('#changeImgType').val(),
        id: '',
        gridPatterns:gridPatterns,
        grid: grid
      },
      contentType: 'application/json; charset=utf-8',
      success: function(result) {
        //$("#div1").html("<img src='static/output/img_bea.png'></img>");
        result = JSON.parse(result);
        subspace = result['dim'];
        var rowPoints = JSON.parse(result['rowPoints']);
        var colPoints = JSON.parse(result['colPoints']);
        var rowPoints_save = JSON.parse(result['rowPoints_save']);
        var colPoints_save = JSON.parse(result['colPoints_save']);
        var allFig= result['allFig'];
        console.log('subspace'+subspace);
        console.log(JSON.parse(result['rowPoints']));
        console.log(JSON.parse(result['colPoints']));
        console.log(JSON.parse(result['dist']), JSON.parse(result['pair']));
        $('#'+mapid).remove();
        $('#'+mapid2).remove();
        $('#'+parent).append('<div id="'+mapid+'" style="width: 500px; height: 400px;"></div>')
        $('#'+parent2).append('<div id="'+mapid2+'" style="width: 500px; height: 400px;"></div>')
        d = new Date();
        if(imgType=='closed') {
        loadImg("/static/output/temp_closed.png?" + d.getTime(),"/static/output/temp_closed_composite.png?" + d.getTime(), 2229, 2058,mapid,mapid2,parent,parent2,'closed');
        $('#loading').html('-');
        var fname = 'output/legend_'+imgType+'.html?' + d.getTime();
        $('#loading').html('-');
        }
        else {
          loadImg("/static/output/temp_heidi.png?" + d.getTime(),"/static/output/temp_heidi_composite.png?" + d.getTime(), 2229, 2058,mapid,mapid2,parent,parent2,'heidi');
          $('#loading').html('-');
          }
        $('#table2').html(convertJsonToTable(JSON.parse(result['rowPoints']),'col'));
        $('#table3').html(convertJsonToTable(JSON.parse(result['colPoints']),'row'));
        //drawGraph(JSON.parse(result['dist']), JSON.parse(result['pair']));
        drawParallelCoordinate('parallelPlot');
        drawGiantWheel('#windrose1');
        $('#pointsPlots').html('');
        console.log('adding crovhd visualization to gui!!');
        $('#crovhd').html('<img src="/static/output/rowColPoints.png?'+ d.getTime() +'">');
        drawPointsComparison('pointsPlots',rowPoints_save,colPoints_save,subspace);
        //uploadHistorgram();
       
      },
      error: function(result) {
        console.log(result);
      }
    });
  });
}


function changeImgType() {

  //console.log('hello');
  var imgType=$(this).val();


  //Plotly.Fx.hover('0_1_#db41e20', [{curveNumber: 0, pointNumber: 0}],
}


function convertJsonToTable(data,type) {
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
      if(key=='id')
      htmlstr2 = htmlstr2.concat("<td id='"+type+'_'+data[i][key]+"'>" + data[i][key] + "</td>");
      else
      htmlstr2 = htmlstr2.concat("<td>" + data[i][key] + "</td>");
      //htmlstr2 = htmlstr2.concat("<td>" + data[i].b + "</td>");
      //htmlstr2 = htmlstr2.concat("<td>" + data[i].c + "</td>");
      //htmlstr2 = htmlstr2.concat("<td>" + data[i].d + "</td>");
    }
    htmlstr2 = htmlstr2.concat('</tr>');
  }
  htmlstr2 = htmlstr2.concat('</table>');
  return htmlstr2;
}

function drawPointsComparison(containerid,rowPoints,colPoints,subspace) {
  console.log(' -- drawPointsComparison start --');
  console.log('INPUTPARAMS');
  console.log(containerid);
  console.log(rowPoints);
  console.log(colPoints);
  var rowId = rowPoints.map(a => a.id);
  var colId = colPoints.map(a => a.id);
  var text = rowId.map(function (num, idx) {
  return num +","+ colId[idx];
  });
  //subspace=[subspace];
  if(typeof(subspace[0])==='string')
    subspace=[subspace];

  for(var i=0;i<subspace.length;i++) {
    var cid=containerid+i;
    $('#'+containerid).append("<div id='" +cid+ "' class='col-sm-4'></div>");
    if(subspace[i].length==1) {
      var trace1 = {
          y: rowPoints.map(a => a[subspace[i]]),
          x: colPoints.map(a => a[subspace[i]]),
          mode: 'markers',
          type: 'scatter',
          name: 'row points',
          text: text,
          marker : {
                  //size : 10,
                  color : containerid.split('_')[2]
                  }
          //text : document.getElementById('hoverinfo')
        };
        var layout = {
            title: '1-d points comparison, subspace : '+subspace[i],
            width:500,
            height:500,
            xaxis: {
              title:'<b> Row Points :'+subspace[i]+' </b>'
           },
           yaxis: {
              title:'<b>Col Points :'+subspace[i]+'</b>'
          },
          //paper_bgcolor:containerid.split('_')[2]
        };
        var myPlot=document.getElementById(containerid);
        var data = [trace1];
        Plotly.newPlot(cid, data, layout);
    }
    else if(subspace[i].length==2) {
      var trace1 = {
          y: rowPoints.map(a => a[subspace[i][0]]),
          x: rowPoints.map(a => a[subspace[i][1]]),
          mode: 'markers',
          type: 'scatter',
          name: 'row points',
          text: text,
          marker : {
                  //size : 10,
                  //color : containerid.split('_')[2]

                  }
          //text : document.getElementById('hoverinfo')
        };
        var trace2 = {
            y: colPoints.map(a => a[subspace[i][0]]),
            x: colPoints.map(a => a[subspace[i][1]]),
            mode: 'markers',
            type: 'scatter',
            name: 'column points',
            text: text,
            marker : {
                    //size : 10,
                    //color : containerid.split('_')[2]

                    }
          };
        var layout = {
            title: "Row Block : "+containerid.split('_')[0]+" Column Block : "+containerid.split('_')[1],
            width:500,
            height:500,
            xaxis: {
              title:'<b>'+subspace[i][0]+'</b>'
           },
           yaxis: {
              title:'<b>'+subspace[i][1]+'</b>'
          },
          //paper_bgcolor:containerid.split('_')[2]
        };
        var myPlot=document.getElementById(containerid);
        var data = [trace1,trace2];
        Plotly.newPlot(cid, data, layout);

    }
    else if(subspace[i].length==3) {
      //DRAW 3-D SCATTER
      var trace1 = {
          y: rowPoints.map(a => a[subspace[i][0]]),
          x: rowPoints.map(a => a[subspace[i][1]]),
          z: rowPoints.map(a => a[subspace[i][2]]),
          mode: 'markers',
          type: 'scatter',
          name: 'row points',
          text: text,
          marker : {
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
            text: text,
            marker : {
                    //size : 10,
                  },
          type: 'scatter3d'
          };

        var layout = {
                        	scene: {
                        		xaxis:{title: subspace[i][0]},
                        		yaxis:{title: subspace[i][1]},
                        		zaxis:{title: subspace[i][2]},
                        		},
                        	autosize: false,
                        	width: 550,
                        	height: 500,

                        };
        var myPlot=document.getElementById(containerid);
        var data = [trace1,trace2];
        Plotly.newPlot(cid, data, layout);
    }
    /*var myPlot=document.getElementById(cid);
    hoverInfo = document.getElementById('hoverinfo');
    myPlot.on('plotly_click', function(data){
        var xaxis = data.points[0].xaxis,
            yaxis = data.points[0].yaxis;
        var infotext = data.points.map(function(d){
          return ('row: '+d.x+', col: '+d.y);
        });
        var index=data.points[0].pointIndex;
        if(flag==1) {
          $('#row_'+col[highlighted_idx]).css({"background-color": "white", "font-size": "100%"});
          $('#col_'+row[highlighted_idx]).css({"background-color": "white", "font-size": "100%"});
        }
        $('#row_'+col[index]).css({"background-color": "yellow", "font-size": "200%"});
        $('#col_'+row[index]).css({"background-color": "yellow", "font-size": "200%"});
        highlighted_idx=index;
        flag=1;
        hoverInfo.innerHTML = infotext.join('');
    })*/

  } //for

  console.log('plots draw finished');

}//fn

function drawGiantWheel(container) {
  console.log(' --drawGiantWheel-- ');
  var inputParam = {};
  inputParam['dataset'] = "static/output/rowColPoints.csv"; //PATH OF DATASET
  inputParam['order'] = [1, 2, 3, 4];
  inputParam['classColumn'] = 5;
  inputParam['colorDict'] = {
    "0": "green",
    "1": "yellow",
    "2": "red"
  };
  inputParam['width'] = 500;
  inputParam['height'] = 500;
  inputParam['container'] = '#windrose1';
  chart_wheel(inputParam);

}

function drawParallelCoordinate(container) {
  d = new Date();
  Plotly.d3.csv('/static/output/rowColPoints.csv?'+d.getTime(), function(err, rows) {
    console.log(colNames);
    function unpack(rows, key) {
      return rows.map(function(row) {
        return row[key];
      });
    }

    var dims=[];
    for (k in colNames) {
      if(k!='id') {
      var t={};
      t['label']=k;
      t['values']=unpack(rows,k);
      dims.push(t);}
    }
    console.log('ddpdpd');
    console.log(dims);

    var data = [{
      type: 'parcoords',
      pad: [80, 80, 80, 80, 80],
      line: {
        color: unpack(rows, 'classLabel'),
        colorscale: [[0, 'red'], [0.5, 'green'], [1, 'blue']]
      },

      dimensions: dims
    }];

    var layout = {
      width: 800
    };

    Plotly.plot(container, data, layout);

  });
}
