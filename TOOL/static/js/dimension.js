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

function loadImg(url, w, h,mapid,parent,imgType) {
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
        /*result = JSON.parse(result);
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
        */
        $('#'+mapid).remove();
        $('#'+parent).append('<div id="'+mapid+'" style="width: 600px; height: 500px;"></div>')
        d = new Date();
        if(imgType=='closed') {
        loadImg("/static/output/temp_closed.png?" + d.getTime(),"/static/output/temp_closed_composite.png?" + d.getTime(), 2229, 2058,mapid,mapid2,parent,parent2,'closed');
        $('#loading').html('-');
        var fname = 'output/legend_'+imgType+'.html?' + d.getTime();
        $('#loading').html('-');
        }
        else {
          loadImg("/static/output/temp_heidi.png?" + d.getTime(), 2229, 2058,mapid,parent,'heidi');
          $('#loading').html('-');
          }
        //$('#table2').html(convertJsonToTable(JSON.parse(result['rowPoints']),'col'));
        //$('#table3').html(convertJsonToTable(JSON.parse(result['colPoints']),'row'));
        
        //drawParallelCoordinate('parallelPlot');
        //drawGiantWheel('#windrose1');
        //$('#pointsPlots').html('');
        //console.log('adding crovhd visualization to gui!!');
        //$('#crovhd').html('<img src="/static/output/rowColPoints.png?'+ d.getTime() +'">');
        //drawPointsComparison('pointsPlots',rowPoints_save,colPoints_save,subspace);
        //uploadHistorgram();
       
      },
      error: function(result) {
        console.log(result);
      }
    });
    
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
      console.log('--success--');
      var result1=JSON.parse(result);
      /*var subspace=result1['subspace'];
      var output=result1['output'];
      var subspaceList="";
      for(var i=0;i<subspace.length;i++) {
        subspaceList = subspaceList.concat('<input type="checkbox" class="subspace" value="' + i + '" name="order_dim" class="order_dim">' + k + '</input>&nbsp;&nbsp;&nbsp;&nbsp;');
      }
      $('#subspace').html(subspaceList);
      */
      $('#mapid').remove();
      //$('#mapid2').remove();
      //$('#mapid3').remove();
      //$('#mapid4').remove();
      $('#parent').append('<div id="mapid" style="width: 600px; height: 500px;"></div>')
      //$('#parent2').append('<div id="mapid2" style="width: 500px; height: 400px;"></div>')
      //$('#parent3').append('<div id="mapid3" style="width: 500px; height: 400px;"></div>')
      //$('#parent4').append('<div id="mapid4" style="width: 500px; height: 400px;"></div>')
      d = new Date();
      loadImg("/static/output/consolidated_img.png?" + d.getTime(), 2229, 2058,'mapid','parent','heidi');
      //loadImg("/static/output/closed_img.png?" + d.getTime(),"/static/output/closed_composite.png?" + d.getTime(), 2229, 2058,'mapid3','mapid4','parent3','parent4','closed');
      $('#loading').html('-');
      var fname = '/static/output/legend_heidi.html?' + d.getTime();
      $('#legend').load(fname);
      //var fname = '/static/output/legend_closed.html?' + d.getTime();
      //$('#legend2').load(fname);
      
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
      $('#parent').append('<div id="mapid" style="width: 600px; height: 500px;"></div>')
      d = new Date();
      loadImg("/static/output/consolidated_img.png?" + d.getTime(), 2229, 2058,'mapid','parent','heidi');
      //loadImg("/static/output/closed_img.png?" + d.getTime(),"/static/output/closed_composite.png?" + d.getTime(), 2229, 2058,'mapid3','mapid4','parent3','parent4','closed');
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