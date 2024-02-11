const MAPBOX_API_KEY = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';

// Initialize map
mapboxgl.accessToken = MAPBOX_API_KEY;
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-84.387982, 33.753746], // Default center coordinates
  zoom: 12, // Default zoom level
});

// Define escalation categories and corresponding colors
const escalationColors = {
  1: 'yellow',
  2: 'pink',
  3: 'red',
  4: 'black',
};

// Fetch patient data from JSON file
fetch('escalation_results.json')
  .then(response => response.json())
  .then(data => {
    // Iterate over each hospital
    for (const hospitalAddress in data.hospitals) {
      const hospital = data.hospitals[hospitalAddress];
      const patients = hospital.patients;

      // Iterate over each patient for this hospital
      patients.forEach(patient => {
        const { latitude, longitude, escalation, first_name, last_name } = patient;

        // Determine marker color based on escalation level
        const color = escalationColors[escalation] || 'gray';

        // Create a new marker for patients
        new mapboxgl.Marker({
          color: color,
        })
          .setLngLat([longitude, latitude])
          .setPopup(new mapboxgl.Popup().setHTML(`<h3>${first_name} ${last_name}</h3><p>Escalation: ${escalation}</p>`))
          .addTo(map);
      });
    }

    // Add legend or key for escalation categories
    const legend = document.createElement('div');
    legend.innerHTML = `
      <h3>Escalation Categories</h3>
      <div><span class="legend-dot" style="background-color: yellow;"></span> Level 1</div>
      <div><span class="legend-dot" style="background-color: pink;"></span> Level 2</div>
      <div><span class="legend-dot" style="background-color: red;"></span> Level 3</div>
      <div><span class="legend-dot" style="background-color: black;"></span> Level 4</div>
    `;
    legend.className = 'mapboxgl-ctrl';
    map.getContainer().appendChild(legend);
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });