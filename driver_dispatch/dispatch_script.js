const MAPBOX_API_KEY = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';
mapboxgl.accessToken = MAPBOX_API_KEY;

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-84.387982, 33.753746],
  zoom: 12
});

// Define escalation categories and corresponding colors
const escalationColors = {
  1: '#ffdb4d',
  2: '#ffa64d',
  3: '#ff8080',
  4: '#ff1a1a',
};

// Function to add a patient to the map
function addPatientToMap(patient) {
  const { latitude, longitude, escalation, first_name, last_name, timestamp, address } = patient;

  // Determine marker color based on escalation level
  const color = escalationColors[escalation] || 'gray';

  // Create a new marker for the patient
  new mapboxgl.Marker({
    color: color,
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${first_name} ${last_name}</h3><p>Address: ${address}</p><p>Timestamp: ${timestamp}</p>`))
    .addTo(map);
}

// Function to add a hospital marker to the map
function addHospitalToMap(hospital) {
  const { latitude, longitude, facility_name, address } = hospital;

  // Create a new hospital marker
  new mapboxgl.Marker({
    color: 'midnightblue', // Dark blue color
    scale: 1.8 // Larger size than the default
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${facility_name}</h3><p>Address: ${address}</p>`)) // Popup with hospital name and address
    .addTo(map);
}

// Fetch patient data from JSON file
fetch('patients_by_hospital.json')
  .then(response => response.json())
  .then(data => {
    // Iterate over each hospital
    Object.values(data.hospitals).forEach(hospital => {
      const patients = hospital.patients;

      // Add hospital to the map
      addHospitalToMap(hospital);

      // Iterate over each patient for this hospital and add them to the map
      patients.forEach(patient => {
        addPatientToMap(patient);
      });
    });

    // Add legend or key for escalation categories
    const legend = document.createElement('div');
    legend.innerHTML = `
      <h3>Escalation Categories</h3>
      <div><span class="legend-dot" style="background-color: #ffdb4d;"></span> Escalation 1</div>
      <div><span class="legend-dot" style="background-color: #ffa64d;"></span> Escalation 2</div>
      <div><span class="legend-dot" style="background-color: #ff8080;"></span> Escalation 3</div>
      <div><span class="legend-dot" style="background-color: #ff1a1a;"></span> Escalation 4</div>
    `;
    legend.className = 'mapboxgl-ctrl legend'; // Add 'legend' class here
    map.getContainer().appendChild(legend);
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });

// Function to update map data based on selected time range
function updateMapData() {
  const currentTime = new Date().toISOString();
  // Your logic to update map data based on current time goes here
  console.log('Current Time:', currentTime);
}
