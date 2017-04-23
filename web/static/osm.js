// set up the map
map = new L.Map('container');

// create the tile layer with correct attribution
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, {
    minZoom: 8,
    maxZoom: 12,
    attribution: osmAttrib
});

// start the map in South-East England
map.setView(new L.LatLng(113.975969, 22.5331), 9);
map.addLayer(osm);
