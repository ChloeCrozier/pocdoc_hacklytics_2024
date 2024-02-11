const MAPBOX_API_KEY = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';
mapboxgl.accessToken = MAPBOX_API_KEY;

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-84.30150675, 33.86447125],
  zoom: 10
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
  const { latitude, longitude, escalation, first_name, last_name, timestamp } = patient;

  // Determine marker color based on escalation level
  const color = escalationColors[escalation] || 'gray';

  // Create a new marker for the patient
  new mapboxgl.Marker({
    color: color,
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${first_name} ${last_name}</h3><p>Address: ${patient.address}</p><p>Timestamp: ${timestamp}</p>`))
    .addTo(map);
}

// Function to add a hospital marker to the map
function addHospitalToMap(hospital) {
  const { latitude, longitude, name, address } = hospital;

  // Create a new hospital marker
  new mapboxgl.Marker({
    color: 'midnightblue', // Dark blue color
    scale: 1.8 // Larger size than the default
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${name}</h3><p>Address: ${address}</p>`)) // Use 'name' variable for hospital name
    .addTo(map);
}

// Fetch patient data from JSON file
fetch('patients_by_hospital.json')
  .then(response => response.json())
  .then(data => {
    // Populate the hospital dropdown menu
    const hospitalsDropdown = document.getElementById('hospital-dropdown');
    Object.values(data.hospitals).forEach(hospital => {
      const option = document.createElement('option');
      option.text = hospital.facility_name;
      option.value = hospital.facility_name;
      hospitalsDropdown.add(option);
    });

    // Add hospital markers and patient markers to the map
    Object.values(data.hospitals).forEach(hospital => {
      addHospitalToMap(hospital);
      hospital.patients.forEach(patient => {
        addPatientToMap(patient);
      });
    });
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });

// Function to update map data based on selected hospitals
function updateMapData() {
  const selectedHospitals = Array.from(document.getElementById('hospital-dropdown').selectedOptions).map(option => option.value);
  console.log('Selected Hospitals:', selectedHospitals);

  // Hide all markers
  map.eachLayer(layer => {
    if (layer instanceof mapboxgl.Marker) {
      layer.remove();
    }
  });

  // Add hospital markers and patient markers for selected hospitals
  fetch('patients_by_hospital.json')
    .then(response => response.json())
    .then(data => {
      Object.values(data.hospitals).forEach(hospital => {
        if (selectedHospitals.includes(hospital.facility_name)) {
          addHospitalToMap(hospital);
          hospital.patients.forEach(patient => {
            addPatientToMap(patient);
          });
        }
      });
    })
    .catch(error => {
      console.error('Error fetching JSON:', error);
    });
}
