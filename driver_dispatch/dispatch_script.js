const MAPBOX_API_KEY = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';
mapboxgl.accessToken = MAPBOX_API_KEY;

let map; // Declare map variable outside any function scope
let markers = []; // Define markers array to store marker references

// Function to initialize the map
function initializeMap() {
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [-84.30150675, 33.86447125],
    zoom: 10
  });
}

// Fetch patient data from JSON file and populate dropdown menu
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

    // Autofill the time select with current date/time subtracted by 5 hours
    autofillTimeSelect();

    // Initialize the map after fetching data and populating dropdown
    initializeMap();

    // Generate map with all data
    generateMap();
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });

// Function to generate map with hospitals and patients
function generateMap(selectedHospitals = [], selectedTime = new Date()) {
  // Remove existing markers
  markers.forEach(marker => marker.remove());
  markers = []; // Clear markers array

  // Fetch patient data from JSON file
  fetch('patients_by_hospital.json')
    .then(response => response.json())
    .then(data => {
      // const hospitalsDropdown = document.getElementById('hospital-dropdown'); // Get hospitals dropdown again
      
      Object.values(data.hospitals).forEach(hospital => {
        
        addHospitalToMap(hospital);
        
        hospital.patients.forEach(patient => {
          const patientTime = new Date(patient.timestamp);
          if ((!selectedTime || patientTime >= selectedTime) && (selectedHospitals.length === 0 || selectedHospitals.includes(hospital.facility_name))) {
            addPatientToMap(patient);
          }
        });
      });
    })
    .catch(error => {
      console.error('Error fetching JSON:', error);
    });
}

// Function to add a patient to the map
function addPatientToMap(patient) {
  const { latitude, longitude, escalation, first_name, last_name, timestamp } = patient;

  // Define escalation categories and corresponding colors
  const escalationColors = {
    1: '#ffdb4d',
    2: '#ffa64d',
    3: '#ff8080',
    4: '#ff1a1a',
  };
  
  // Determine marker color based on escalation level
  const color = escalationColors[escalation] || 'gray';

  // Create a new marker for the patient
  const marker = new mapboxgl.Marker({
    color: color,
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${first_name} ${last_name}</h3><p>Address: ${patient.address}</p><p>Timestamp: ${timestamp}</p>`))
    .addTo(map);
  
  markers.push(marker); // Add marker to markers array
}

// Function to add a hospital marker to the map
function addHospitalToMap(hospital) {
  const { latitude, longitude, facility_name, address } = hospital;

  // Create a new hospital marker
  const marker = new mapboxgl.Marker({
    color: '#009E60', 
    scale: 1.8 // Larger size than the default
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${facility_name}</h3><p>Address: ${address}</p>`)) // Use 'name' variable for hospital name
    .addTo(map);

  // Add event listener to show hospital name on hover
  // marker.getElement().addEventListener('mouseenter', () => {
  //   // You can replace the console.log with any action you want, such as displaying the hospital name in a tooltip
  // });
}

// Function to handle filter application
function applyFilters() {
  const selectedHospitals = Array.from(document.getElementById('hospital-dropdown').selectedOptions).map(option => option.value);
  const selectedTime = new Date(document.getElementById('start-time').value);
  generateMap(selectedHospitals, selectedTime);
}

// Autofill the time select with current date/time subtracted by 5 hours
function autofillTimeSelect() {
  const currentTime = new Date();
  currentTime.setHours(currentTime.getHours() - 5); // Subtract 5 hours
  const formattedTime = currentTime.toISOString().slice(0, 16);
  document.getElementById('start-time').value = formattedTime;
}
