var map;
var visibleLocations = [];
var maxLocations = 5;

function initialize() {
    var latlng = new google.maps.LatLng(43.03, -75.38);
    var options = {
        zoom: 8,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        options);
}

function get_bounding_box_points() {
    var maxLat = -90.0;
    var minLat = 90.0;
    var maxLong = -180.0;
    var minLong = 180.0;
    // loop through visible markers;
    for (i=0; i<visibleLocations.length; i++) {
        var locLat = visibleLocations[i].locLat;
        var locLong = visibleLocations[i].locLong;
        if (locLat > maxLat) { maxLat = locLat; }
        else if (locLat < minLat) { minLat = locLat; }
        if (locLong > maxLong) { maxLong = locLong; }
        else if (locLong < minLong) { minLong = locLong; }
    }
    return {'maxLat':maxLat, 'minLat':minLat, 'maxLong':maxLong, 'minLong':minLong} ;
}

function update_map(received_msg) {
    var newLat = received_msg.locLat;
    var newLong = received_msg.locLong;
    var newLoc = new google.maps.LatLng(newLat,newLong);
    map.setCenter(newLoc);
    var marker = new google.maps.Marker({
        position: newLoc, 
        map: map
    });
    newLocDict = {
        'locLat':newLat,
        'locLong':newLong
    };
    if (visibleLocations.length >= maxLocations) {
        visibleLocations.shift();
    }
    visibleLocations.push(newLocDict);
    console.log(received_msg);
    console.log(visibleLocations);
    if (visibleLocations.length > 1) {
        var bounds = get_bounding_box_points();
        var SW = new google.maps.LatLng(bounds.minLat, bounds.minLong);
        var NE = new google.maps.LatLng(bounds.maxLat, bounds.maxLong);
        var mapBounds = new google.maps.LatLngBounds(SW, NE);
        map.fitBounds(mapBounds);
    }
}

function start_web_socket() {
    if ("WebSocket" in window) {
        var ws = new WebSocket("ws://50.16.101.124/realtime/");
        ws.onopen = function() {};
        ws.onmessage = function(evt) {
            var received_msg = JSON.parse(evt.data);
            update_map(received_msg);
        };
        ws.onclose = function() {};
    } else {
        alert("no websockets, sorry!");
    }
}

