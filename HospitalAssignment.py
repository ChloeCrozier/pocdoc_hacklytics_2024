import pandas as pd
import numpy as np

def distance_squared(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

import json

# Load hospital and patient datasets
hospital_data = pd.read_csv('hospital_locations.csv')
patient_data = pd.read_csv('patients.csv')

# Function to assign patients to hospitals based on distance
def assign_patients_to_hospitals(hospitals, patients):
    assignments = {}
    for _, hospital in hospitals.iterrows():
        hospital_address = hospital['address']
        assignments[hospital_address] = {
            "address": hospital['address'],
            "longitude": hospital['longitude'],
            "latitude": hospital['latitude'],
            "num_vans": [],
            "van_ratio": [],
            "score": hospital['score'],
            "hospital": ['facility_name']
        }

    for _, patient in patients.iterrows():
        min_distance = np.inf
        assigned_hospital_address = None
        for _, hospital in hospitals.iterrows():
            dist_sq = distance_squared(patient['latitude'], patient['longitude'], hospital['latitude'], hospital['longitude'])
            if dist_sq < min_distance:
                min_distance = dist_sq
                assigned_hospital_address = hospital['address']

        if assigned_hospital_address:
            assignments[assigned_hospital_address]['hospital'].append({
                "latitude": patient['latitude'],
                "longitude": patient['longitude'],
                "escalation": patient['escalation'],
                "first_name": patient['first_name'],
                "last_name": patient['last_name'],
                "Time_Stamp": patient['timestamp'],
                "address": []
            })

    return assignments

# Assign patients to hospitals
patient_assignments = assign_patients_to_hospitals(hospital_data, patient_data)

# Write to JSON file
with open('hospital_patient_assignments.json', 'w') as json_file:
    json.dump(patient_assignments, json_file, indent=4)
