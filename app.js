// Initialize the map and set its view to a specific location and zoom level
var map = L.map('map').setView([20, 0], 2); // Centered on the equator

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variable to hold the current marker
var currentMarker = null;

// Initialize geocoder for searching locations
var geocoder = L.Control.Geocoder.nominatim();

// Function to add marker and popup
function addMarkerToMap(latlng, name) {
    if (currentMarker) {
        map.removeLayer(currentMarker);
    }
    currentMarker = L.marker(latlng).addTo(map);
    currentMarker.bindPopup("Location: " + name).openPopup();
    map.setView(latlng, 13);
}

// Get DOM elements
var searchInput = document.getElementById('search-input');
var autocompleteResults = document.getElementById('autocomplete-results');

// Handle search input with autocomplete
searchInput.addEventListener('input', function() {
    var query = this.value;
    if (query.length > 2) {
        geocoder.geocode(query, function(results) {
            autocompleteResults.innerHTML = '';
            results.forEach(function(result) {
                var div = document.createElement('div');
                div.textContent = result.name;
                div.addEventListener('click', function() {
                    addMarkerToMap(result.center, result.name);
                    searchInput.value = result.name;
                    autocompleteResults.style.display = 'none';
                });
                autocompleteResults.appendChild(div);
            });
            autocompleteResults.style.display = results.length > 0 ? 'block' : 'none';
        });
    } else {
        autocompleteResults.style.display = 'none';
    }
});

// Handle search input on enter key
searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        var query = this.value;
        geocoder.geocode(query, function(results) {
            if (results.length > 0) {
                var result = results[0];
                addMarkerToMap(result.center, result.name);
                autocompleteResults.style.display = 'none';
            }
        });
    }
});

// Close autocomplete results when clicking outside
document.addEventListener('click', function(e) {
    if (e.target !== searchInput && e.target !== autocompleteResults) {
        autocompleteResults.style.display = 'none';
    }
});

// Handle map click
map.on('click', function(e) {
    geocoder.reverse(e.latlng, map.options.crs.scale(map.getZoom()), function(results) {
        var r = results[0];
        if (r) {
            addMarkerToMap(e.latlng, r.name);
            searchInput.value = r.name;
        }
    });
});

