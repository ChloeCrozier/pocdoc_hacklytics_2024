const MAPBOX_API_KEY = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';

// Initialize map
mapboxgl.accessToken = MAPBOX_API_KEY;
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-84.387982, 33.753746], // Default center coordinates
  zoom: 12, // Default zoom level
});

// Fetch patient data from JSON file
fetch('escalation_results.json')
  .then(response => response.json())
  .then(data => {
    // Iterate over each address
    for (const address in data) {
      const { patients } = data[address];
      const isHospital = address === "705 DIXIE STREET" || address === "80 JESSE HILL, JR DRIVE SE" || address === "550 PEACHTREE STREET, NE";

      // If the address is a hospital, create a larger dark blue marker
      if (isHospital) {
        const { latitude, longitude } = data[address];
        new mapboxgl.Marker({
          color: 'darkblue',
          scale: 1.5, // Increase the marker size
        })
          .setLngLat([longitude, latitude])
          .addTo(map);
      }

      // Iterate over each patient
      patients.forEach(patient => {
        const { latitude, longitude, escalation, first_name, last_name } = patient;

        // Determine marker color based on escalation level
        let color;
        switch (escalation) {
          case 1:
            color = 'yellow';
            break;
          case 2:
            color = 'pink';
            break;
          case 3:
            color = 'red';
            break;
          case 4:
            color = 'black';
            break;
          default:
            color = 'gray';
        }

        // Create a new marker
        new mapboxgl.Marker({
          color: color,
        })
          .setLngLat([longitude, latitude])
          .setPopup(new mapboxgl.Popup().setHTML(`<h3>${first_name} ${last_name}</h3><p>Escalation: ${escalation}</p>`))
          .addTo(map);
      });
    }
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });

const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});