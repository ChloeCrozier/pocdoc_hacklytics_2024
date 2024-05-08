document.addEventListener('DOMContentLoaded', function () {
    // Example severity level passed via query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const severity = urlParams.get('severity');
    const location = urlParams.get('location') || 'Atlanta, GA'; // Default location


    // Initialize the map
    mapboxgl.accessToken = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [-84.3880, 33.7490], // Coordinates for Atlanta, GA as a default
        zoom: 10
    });

    // Add a marker for a dummy clinic location
    new mapboxgl.Marker()
        .setLngLat([-84.3880, 33.7490])
        .addTo(map);
});
