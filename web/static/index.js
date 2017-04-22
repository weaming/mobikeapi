var map = new AMap.Map('container', {
    resizeEnable: true,
    zoom: 12,
    center: [113.975969, 22.5331]
});

function set_bike(x) {
    new AMap.Marker({
        showPositionPoint: true,
        map: map,
        position: x,
    });
}

var locations = fetch('/api/bikes')
    .then(resp => resp.json())
    .then(function(locations) {
        console.log('bikes:', locations.length)
        locations.forEach(function(x) {
            var location = new AMap.LngLat(x.distX, x.distY);
            set_bike(location);
        });
    })
