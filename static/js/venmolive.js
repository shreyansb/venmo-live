var map;
var visibleMarkers = [];
var maxMarkers = 5;
var signupIcon = 'static/assets/mario-jumping-icon.png';
var payIcon = 'static/assets/money-bag-icon.png';
var chargeIcon = 'static/assets/money-bag-icon.png';
var commentIcon = 'static/assets/money-bag-icon.png';

function initialize() {
    var venmoOffice = new google.maps.LatLng(40.7457, -73.9935);
    var options = {
        zoom: 12,
        center: venmoOffice,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        options);
}

function new_loc_from_message(received_msg) {
    var newLat = received_msg.locLat;
    var newLong = received_msg.locLong;
    if (!newLat || !newLong) { return; }
    var newLoc = new google.maps.LatLng(newLat,newLong);
    return newLoc;
}

function get_bounding_box_points() {
    var locLats = [];
    var locLongs = [];
    // loop through visible markers;
    for (i=0; i<visibleMarkers.length; i++) {
        var position = visibleMarkers[i].getPosition();
        locLats.push(position.lat());
        locLongs.push(position.lng());
    }
    var points =  {
        'maxLat':Math.max.apply(null, locLats), 
        'minLat':Math.min.apply(null, locLats),
        'maxLong':Math.max.apply(null, locLongs), 
        'minLong':Math.min.apply(null, locLongs)
    };
    return points;
}

function create_marker(newLoc, locType) {
    var markerOptions = {
        position: newLoc, 
        map: map,
        animation: google.maps.Animation.DROP
    };
    if (locType == 'pay') {
        markerOptions.icon = payIcon;
    } else if (locType == 'charge') {
        markerOptions.icon = chargeIcon;
    } else if (locType == 'signup_detailed') {
        markerOptions.icon = signupIcon;
    } else if (locType == 'comment') {
        markerOptions.icon = commentIcon;
    }
    return new google.maps.Marker(markerOptions);
}

function update_map(newLoc, locType) {
    map.setCenter(newLoc);
    var marker = create_marker(newLoc, locType);
    if (visibleMarkers.length >= maxMarkers) {
        var removedMarker = visibleMarkers.shift();
        removedMarker.setMap(null);
    }
    visibleMarkers.push(marker);
    if (visibleMarkers.length > 1) {
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
            console.log(received_msg);
            render_template(received_msg);
            var newLoc = new_loc_from_message(received_msg);
            var locType = received_msg.cat;
            update_map(newLoc, locType);
        };
        ws.onclose = function() {};
    } else {
        alert("no websockets, sorry!");
    }
}

function render_template(data) {
    if ( data.cat == "pay" || data.cat == "charge" ){
        if ("note" in data && data.note != undefined) {
            /* Public Payment */
            var from_profile_pic = data.from_user_img_url;
            var to_profile_pic = data.to_user_img_url;
            var note = data.note;
            var public_payment = '<li class="public_payment shadow">';
            public_payment += '<span class="date">'+data.cat+'</span>';
            public_payment += '<div class="pics clearfix">';
            public_payment += '<img height="50px" class="profile_pic shadow float_left" src="'+from_profile_pic+'" />';
            public_payment += '<img height="50px" class="profile_pic shadow float_right" src="'+to_profile_pic+'" />';
            public_payment += '<span class="note shadow float_right">'+note+'</span>';
            public_payment += '</div>';
            public_payment += '</li>';
            $("#events ul").prepend($(public_payment));
        }
        else {
            /* Private Payment */
            var public_payment = '<li class="private_payment">';
            public_payment += '<span class="date">Payment</span>';
            public_payment += '<span class="note">Private - $'+data.amount+'</span>';
            public_payment += '</li>';
            $("#events ul").prepend($(public_payment));
        }
    }
    else if (data.cat == "signup_detailed") {
        var public_payment = '<li class="sign_up shadow">';
        public_payment += '<span class="date">New User</span>';
        public_payment += '<div class="pics clearfix">';
        public_payment += '<img height="50px" class="profile_pic shadow float_left" src="'+data.profile_picture+'" />';
        public_payment += '<span class="note shadow float_right">'+data.user+' just signed up!</span>';
        public_payment += '</div>';
        public_payment += '</li>';
        $("#events ul").prepend($(public_payment));
    }
}
