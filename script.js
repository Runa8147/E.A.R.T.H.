// Initialize the map
var mymap = L.map('map').setView([51.505, -0.09], 13); // Adjust initial location

// Add tile layer (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

// Event listener for adding markers
document.getElementById('add-marker').addEventListener('click', function() {
    var imageTag = document.getElementById('image-tag').value;
    var description = document.getElementById('description').value;

    // Get current mouse position on the map
    var latlng = mymap.mouseEventToLatLng(mymap.mouseEvent);

    // Create marker with image tag and description
    var marker = L.marker(latlng).addTo(mymap);
    marker.bindPopup("<b>Image Tag:</b> " + imageTag + "<br><b>Description:</b> " + description); 
});