var filterList = new Set();
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
        htmlstr = htmlstr.concat('<input type="checkbox" class="dim" value="' + i + '">' + k + '<br>');
        //htmlstr2 = htmlstr2.concat('<input type="radio" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;')
        htmlstr2 = htmlstr2.concat('<input type="checkbox" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
        i++;
      }
    }
    $(divId1).html(htmlstr);
    $(divId2).html(htmlstr2);
  }

function colorFilter() {
  console.log(this, $(this).attr('bgcolor'));
  console.log('hello');
  $('#loading').html('<img src="static/image/loading.gif"> loading...');
  $.ajax({
    url: "/redrawimg",
    data: {
      color_value: $(this).attr('bgcolor'),
      datasetPath: getParameterByName('datasetPath')
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      //$("#div1").html("<img src='static/output/img_bea.png'></img>");
      console.log(result);
      $('#mapid').remove();
      $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
      d = new Date();
      loadImg("/static/output/temp.png?" + d.getTime(), 2229, 2058);
      $('#loading').html('-');
      var fname = 'output/legend.html?' + d.getTime();
      console.log('loading legend');
      $('#legend').load("{{ url_for('static',filename='fname') }}".replace('fname', fname));
      $('#loading').html('-');
      console.log('legend loaded succesfully');

    }
  });
}

function updateImage() {
  console.log('--updateImage called--');
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

  //var orderDim = $(".order_dim:checked").val();
  var grid = $("input[name=grid]:checked").val();
  var filterDict = {};
  console.log(dimList, orderDim, filterList, grid);
  $('#loading').html('<img src="loading.gif"> loading...');
  filterList.forEach(function(d) {
    filterDict[d] = $('#' + d).val();
  });
  console.log(filterDict);
  $.ajax({
    url: "/image",
    data: {
      order_dim: orderDim,
      selectedDim: dimList,
      filterDict: JSON.stringify(filterDict),
      datasetPath: getParameterByName('datasetPath'),
      grid: grid
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      var result1=JSON.parse(result);
      var subspace=result1['subspace'];
      var output=result1['output'];
      var subspaceList="";
      for(var i=0;i<subspace.length;i++) {
        subspaceList = subspaceList.concat('<input type="checkbox" class="subspace" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
      }
      $('#subspace').html(subspaceList);
      $('#mapid').remove();
      $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
      d = new Date();
      loadImg("/static/output/consolidated_img.png?" + d.getTime(), 2229, 2058);
      $('#loading').html('-');
      var fname = '/static/output/legend.html?' + d.getTime();
      $('#legend').load(fname);
      //$('#legend').load("{{ url_for('static',filename='fname') }}".replace('fname', fname));
    }
  });
}

function resetImage() {
  console.log('--reset image --');
  $('#loading').html('<img src="loading.gif"> loading...');
  var grid = $("input[name=grid]:checked").val();
  $.ajax({
    url: "/resetImage",
    data: {
      datasetPath: getParameterByName('datasetPath'),
      grid: grid
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
      $('#subspace').html(subspaceList);
      $('#mapid').remove();
      $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
      d = new Date();
      console.log('loading image');
      loadImg("/static/output/consolidated_img.png?" + d.getTime(), 2229, 2058);
      console.log('image loaded succesfully');
      $('#loading').html('-');
      var fname = '/static/output/legend.html?' + d.getTime();
      console.log('loading legend');
      //$('#legend').load("{{ url_for('static',filename='fname') }}".replace('fname', fname));
      $.get(fname,function(d) {
        //console.log(d);
        var d1='<form action="/dashboard2" method="get" target="_blank"> <div>Blockwise? <input type="radio" value="yes" name="blockwise">yes<input type="radio" value="no" name="blockwise">no</div> <input type="hidden" name="datasetName" value="'+getParameterByName('datasetPath')+'">'+d+'<input type="submit" value="Submit"></form>';
        $('#legend').html(d1);
        console.log(d1);
      },'html');
      console.log('legend loaded succesfully');

    }
  });

}

function loadImg(url, w, h) {
  var MIN_ZOOM = -1;
  var MAX_ZOOM = 5;
  var INITIAL_ZOOM = 1;
  var ACTUAL_SIZE_ZOOM = 3;
  var map = L.map('mapid', {
    minZoom: MIN_ZOOM,
    maxZoom: MAX_ZOOM,
    center: [0, 0],
    zoom: INITIAL_ZOOM,
    crs: L.CRS.Simple
  });


  var southWest = map.unproject([0, h], ACTUAL_SIZE_ZOOM);
  var northEast = map.unproject([w, 0], ACTUAL_SIZE_ZOOM);
  console.log(southWest, northEast);
  var bounds = new L.LatLngBounds(southWest, northEast);

  L.imageOverlay(url, bounds).addTo(map);



  map.setMaxBounds(bounds);
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
        id: '',
        gridPatterns:gridPatterns,
        grid: grid
      },
      contentType: 'application/json; charset=utf-8',
      success: function(result) {
        //$("#div1").html("<img src='static/output/img_bea.png'></img>");
        result = JSON.parse(result);
        subspace = result['dim'].split(" ");
        console.log('subspace'+subspace);
        console.log(JSON.parse(result['rowPoints']));
        console.log(JSON.parse(result['colPoints']));
        console.log(JSON.parse(result['dist']), JSON.parse(result['pair']));
        $('#mapid').remove();
        $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
        d = new Date();
        loadImg("/static/output/temp.png?" + d.getTime(), 2229, 2058);
        $('#loading').html('-');
        var fname = 'output/legend.html?' + d.getTime();
        $('#legend').load("{{ url_for('static',filename='fname') }}".replace('fname', fname));
        $('#loading').html('-');
        $('#table2').html(convertJsonToTable(JSON.parse(result['rowPoints']),'col'));
        $('#table3').html(convertJsonToTable(JSON.parse(result['colPoints']),'row'));
        //drawGraph(JSON.parse(result['dist']), JSON.parse(result['pair']));
        drawParallelCoordinate('parallelPlot');
        drawGiantWheel('#windrose1');
        drawPointsComparison(subspace, 'pointsPlot1', 'pointsPlot2');

      }
    });
  });
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

function drawPointsComparison(dim, container1, container2) {
  console.log('dim is ' + dim);
  d = new Date();
  var rowFile = "/static/output/rowPoints.csv?" + d.getTime();
  var colFile = "/static/output/colPoints.csv?" + d.getTime();
  var rowColFile = "/static/output/rowColPoints.csv?" + d.getTime();
  var inputParam = {};
  inputParam['rowFile'] = rowFile; //PATH OF DATASET
  inputParam['colFile'] = colFile;
  inputParam['dim'] = dim[0];
  //inputParam['colorDict']={"0":"green","1":"yellow","2":"red"};
  inputParam['width'] = 600;
  inputParam['height'] = 400;
  inputParam['container'] = container1;
  console.log('drawing plots');
  chart_vis3(inputParam);
  inputParam['rowColFile'] = rowColFile;
  inputParam['width'] = 600;
  inputParam['height'] = 400;
  inputParam['container'] = container2;
  inputParam['dim'] = dim;
  chart_vis4(inputParam);
  console.log('plots draw finished');

}

function drawGiantWheel(container) {
  console.log(' --drawGiantWheel-- ');
  var inputParam = {};
  inputParam['dataset'] = "static/output/rowColPoints.csv"; //PATH OF DATASET
  inputParam['order'] = [1, 2, 3, 4, 5];
  inputParam['classColumn'] = 6;
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
