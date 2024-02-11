function generate_map(updateMapData, filters) {
    // If no filters provided, use current time and display all data
    if (!filters) {
      const currentTime = new Date();
      updateMapData({ currentTime: currentTime, selectedHospitals: [] });
      return;
    }
  
    // Extract filters
    const currentTime = filters.currentTime || new Date();
    const selectedHospitals = filters.selectedHospitals || [];
  
    // Fetch patient data from JSON file
    fetch('patients_by_hospital.json')
      .then(response => response.json())
      .then(data => {
        // Add hospital markers and patient markers to the map
        Object.values(data.hospitals).forEach(hospital => {
          if (selectedHospitals.length === 0 || selectedHospitals.includes(hospital.facility_name)) {
            addHospitalToMap(hospital);
            hospital.patients.forEach(patient => {
              const patientTime = new Date(patient.timestamp);
              if (patientTime >= currentTime) {
                addPatientToMap(patient);
              }
            });
          }
        });
      })
      .catch(error => {
        console.error('Error fetching JSON:', error);
      });
  
    // Call updateMapData with the provided filters
    updateMapData({ currentTime: currentTime, selectedHospitals: selectedHospitals });
  }
  
  // Function to add a patient to the map
  function addPatientToMap(patient) {
    const { latitude, longitude, escalation, first_name, last_name, timestamp } = patient;
    const color = escalationColors[escalation] || 'gray'; // Define escalation colors (if not already defined)
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
    new mapboxgl.Marker({
      color: '#009E60', // Dark blue color
      scale: 1.8 // Larger size than the default
    })
      .setLngLat([longitude, latitude])
      .setPopup(new mapboxgl.Popup().setHTML(`<h3>${name}</h3><p>Address: ${address}</p>`))
      .addTo(map);
  }
  