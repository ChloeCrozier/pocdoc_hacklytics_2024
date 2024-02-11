const MAPBOX_API_KEY = 'pk.eyJ1IjoiY3Njcm96aSIsImEiOiJjbHNnNnNyYnUxcjVtMmpvMmIzenFvOXU3In0.RssM7K5M-4FJef1LsPuwcw';
mapboxgl.accessToken = MAPBOX_API_KEY;

let map;
let markers = [];
let hospitalsData; // Store hospitals data globally
let applyTimeConstraint = false; // Set initial value to false

function initializeMap() {
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [-84.30150675, 33.86447125],
    zoom: 10
  });
}

fetch('assigned_units.json')
  .then(response => response.json())
  .then(data => {
    hospitalsData = data.hospitals; // Store hospitals data globally
    const hospitalsDropdown = document.getElementById('hospital-dropdown');
    Object.values(data.hospitals).forEach(hospital => {
      const option = document.createElement('option');
      option.text = hospital.facility_name;
      option.value = hospital.facility_name;
      hospitalsDropdown.add(option);
    });

    initializeMap();
    generateMap();
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });

  function generateMap(selectedHospitals = [], selectedUnits = [], selectedTime = new Date(), applyTimeConstraint = true) {
    markers.forEach(marker => marker.remove());
    markers = [];
    
    Object.values(hospitalsData).forEach(hospital => {
      addHospitalToMap(hospital);
    
      hospital.units.forEach(unit => {
        addUnitToMap(unit, hospital.facility_name);
      });
    
      hospital.units.forEach(unit => {
        unit.patients.forEach(patient => {
          const patientTime = new Date(patient.timestamp);
    
          // If time constraint is enabled and patient's time is before the selected time, skip adding the patient
          if (!applyTimeConstraint && (selectedTime && patientTime < selectedTime)) {
            return;
          } else if ((selectedHospitals.length === 0 || selectedHospitals.includes(hospital.facility_name)) && (selectedUnits.length === 0 || selectedUnits.includes(unit.unit_name))) {
            addPatientToMap(patient);
          }
        });
      });
    });
  }
  
  
  

function addPatientToMap(patient) {
  const { latitude, longitude, escalation, first_name, last_name, timestamp, urgency } = patient;

  const escalationColors = {
    1: '#ffdb4d',
    2: '#ffa64d',
    3: '#ff8080',
    4: '#ff1a1a',
  };
  
  const color = escalationColors[escalation] || 'gray';

  const marker = new mapboxgl.Marker({
    color: color,
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${first_name} ${last_name}</h3><p>Address: ${patient.address}</p><p>Timestamp: ${timestamp}</p><p>Escalation Level: ${escalation}</p>`))
    .addTo(map);
  
  markers.push(marker);
}

function addHospitalToMap(hospital) {
  const { latitude, longitude, facility_name, address } = hospital;

  if (isNaN(latitude) || isNaN(longitude)) {
    console.error(`Invalid latitude or longitude for ${facility_name}`);
    return;
  }

  const marker = new mapboxgl.Marker({
    color: '#009E60',
    scale: 1.8
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${facility_name}</h3><p>Facility Name: ${facility_name}</p><p>Address: ${address}</p>`))
    .addTo(map);
}

function addUnitToMap(unit, hospitalName) {
  const { latitude, longitude, unit_name, patients } = unit;

  const marker = new mapboxgl.Marker({
    color: '#9FE2BF',
  })
    .setLngLat([longitude, latitude])
    .setPopup(new mapboxgl.Popup().setHTML(`<h3>${unit_name} - ${hospitalName}</h3><p>Latitude: ${latitude}</p><p>Longitude: ${longitude}</p><p>Number of patients: ${patients.length}</p>`))
    .addTo(map);
}

function populateUnitDropdown(selectedHospitals) {
  const unitDropdown = document.getElementById('unit-dropdown');
  unitDropdown.innerHTML = '';
  const units = new Set();

  selectedHospitals.forEach(hospitalName => {
    const hospital = hospitalsData.find(data => data.facility_name === hospitalName);
    hospital.units.forEach(unit => {
      units.add(unit.unit_name);
    });
  });

  units.forEach(unit => {
    const option = document.createElement('option');
    option.text = unit;
    option.value = unit;
    unitDropdown.add(option);
  });
}

function applyFilters() {
  const selectedHospitals = Array.from(document.getElementById('hospital-dropdown').selectedOptions).map(option => option.value);
  const selectedUnits = Array.from(document.getElementById('unit-dropdown').selectedOptions).map(option => option.value);
  const selectedTime = new Date(document.getElementById('start-time').value);
  const applyTimeConstraint = document.getElementById('time-constraint-checkbox').checked; // Toggle time constraint based on checkbox state
  generateMap(selectedHospitals, selectedUnits, selectedTime, applyTimeConstraint);
}



function autofillTimeSelect() {
  const currentTime = new Date();
  currentTime.setHours(currentTime.getHours() - 5);
  const formattedTime = currentTime.toISOString().slice(0, 16);
  document.getElementById('start-time').value = formattedTime;
}



autofillTimeSelect();
