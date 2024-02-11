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
hospital_data = pd.read_csv('hospitals.csv')

# Load patient data from JSON file
with open('prompt_results.json', 'r') as json_file:
    patient_data = json.load(json_file)['patients']

# Function to assign patients to hospitals based on distance
def assign_patients_to_hospitals(hospitals, patients):
    assignments = {}
    for _, hospital in hospitals.iterrows():
        hospital_address = hospital['address']
        assignments[hospital_address] = {
            "num_vans": 1,
            "van_ratio": {"General": 0, "Specialized": 0},
            "latitude": hospital['latitude'],
            "longitude": hospital['longitude'],
            "patients": []
        }

    for patient in patients:
        min_distance = np.inf
        assigned_hospital_address = None
        for _, hospital in hospitals.iterrows():
            dist_sq = distance_squared(patient['latitude'], patient['longitude'], hospital['latitude'], hospital['longitude'])
            if dist_sq < min_distance:
                min_distance = dist_sq
                assigned_hospital_address = hospital['address']

        if assigned_hospital_address:
            assignments[assigned_hospital_address]['patients'].append({
                "latitude": patient['latitude'],
                "longitude": patient['longitude'],
                "escalation": patient['escalation'],
                "first_name": patient['first_name'],
                "last_name": patient['last_name'],
                "timestamp": patient['timestamp']
            })

    # Calculate van ratio
    for hospital_address, hospital_assignment in assignments.items():
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
for hospital_address, hospital_info in patient_assignments['hospitals'].items():
    # Get hospital information from the hospital_data dataframe using the address
    hospital_row = hospital_data[hospital_data['address'] == hospital_address].iloc[0]
    
    num_assigned_patients = len(hospital_info['patients'])
    
    # Remove commas and convert population_density to float
    population_density = float(hospital_row['population_density'].replace(',', ''))
    
    # Calculate the number of vans based on the formula provided
    num_vans = math.ceil((num_assigned_patients * num_assigned_patients) / (population_density))
    
    # Update the num_vans for this hospital
    patient_assignments['hospitals'][hospital_address]['num_vans'] = num_vans


# Write to JSON file
with open('patients_by_hospital.json', 'w') as json_file:
    json.dump(patient_assignments, json_file, indent=4)
