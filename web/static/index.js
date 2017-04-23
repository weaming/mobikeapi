var map = new AMap.Map('container', {
    resizeEnable: true,
    zoom: 12,
    center: [113.975969, 22.5331]
});

var last_markders = [];

function set_bike(x) {
    var marker = new AMap.Marker({
        showPositionPoint: true,
        map: map,
        position: x.location,
        icon: '/static/icons/' + x.type + '.png',
    });
    last_markders.push(marker);
}

function fetch_data(center) {
    // clean
    last_markders.forEach(x => {
        x.hide();
        delete(x)
    });
    var url = '/api/bikes'
    if (center) {
        var lng = center.lng,
            lat = center.lat;
        var url = `/api/bikes?lng=${lng}&lat=${lat}`
    }
    var locations = fetch(url)
        .then(resp => resp.json())
        .then(function(locations) {
            console.log('bikes:', locations.length)

            locations.forEach(function(x) {
                var location = new AMap.LngLat(x.distX, x.distY);
                var marker = set_bike({
                    location: location,
                    type: x.biketype
                });
            });
        })
}

function on_drag(center) {
    fetch_data(center);
}

map.on('dragend', () => on_drag(map.getCenter()));

