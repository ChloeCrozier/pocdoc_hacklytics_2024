import pandas as pd
import numpy as np
import json
import math

def distance_squared(x1, y1, x2, y2):
    """
    Calculate the squared distance between two points.
    """
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

# Load hospital dataset
hospital_data = pd.read_csv('../driver_dispatch/hospitals.csv')

# Load patient data from JSON file
with open('../driver_dispatch/prompt_results.json', 'r') as json_file:
    patient_data = json.load(json_file)['patients']

def assign_patients_to_hospitals(hospitals, patients):
    assignments = {}
    for _, hospital in hospitals.iterrows():
        hospital_name = hospital['facility_name']
        assignments[hospital_name] = {
            "facility_name": hospital_name,
            "address": hospital['address'],
            "num_vans": 1,
            "van_ratio": {"General": 0, "Specialized": 0},
            "latitude": hospital['latitude'],
            "longitude": hospital['longitude'],
            "patients": []
        }

    for patient in patients:
        min_distance = np.inf
        assigned_hospital_name = None
        for _, hospital in hospitals.iterrows():
            dist_sq = distance_squared(patient['latitude'], patient['longitude'], hospital['latitude'], hospital['longitude'])
            if dist_sq < min_distance:
                min_distance = dist_sq
                assigned_hospital_name = hospital['facility_name']

        if assigned_hospital_name:
            assignments[assigned_hospital_name]['patients'].append({
                "latitude": patient['latitude'],
                "longitude": patient['longitude'],
                "escalation": patient['escalation'],
                "first_name": patient['first_name'],
                "last_name": patient['last_name'],
                "timestamp": patient['timestamp'],
                "address": 'N/A'
            })

    # Calculate van ratio
    for hospital_name, hospital_assignment in assignments.items():
        total_assigned_patients = len(hospital_assignment['patients'])
        if total_assigned_patients != 0:
            van_counts = {"General": 0, "Specialized": 0}
            for patient in hospital_assignment['patients']:
                if patient['escalation'] == 2:
                    van_counts['General'] += 1
                elif patient['escalation'] == 3:
                    van_counts['Specialized'] += 1
            hospital_assignment['van_ratio']['General'] = van_counts['General'] / total_assigned_patients
            hospital_assignment['van_ratio']['Specialized'] = van_counts['Specialized'] / total_assigned_patients

    return {"hospitals": assignments}


# Assign patients to hospitals
patient_assignments = assign_patients_to_hospitals(hospital_data, patient_data)


# Loop through the hospitals and calculate num_vans for every hospital
for hospital_name, hospital_info in patient_assignments['hospitals'].items():  # Change hospital_address to hospital_name
    # Get hospital information from the hospital_data dataframe using the address
    hospital_row = hospital_data[hospital_data['facility_name'] == hospital_name].iloc[0]
    
    num_assigned_patients = len(hospital_info['patients'])
    
    # Remove commas and convert population_density to float
    population_density = float(hospital_row['population_density'].replace(',', ''))
    
    # Calculate the number of vans based on the formula provided
    num_vans = math.ceil((num_assigned_patients * num_assigned_patients) / (population_density))
    
    # Update the num_vans for this hospital
    patient_assignments['hospitals'][hospital_name]['num_vans'] = num_vans


# Write to JSON file
with open('../driver_dispatch/patients_by_hospital.json', 'w') as json_file:
    json.dump(patient_assignments, json_file, indent=4)
