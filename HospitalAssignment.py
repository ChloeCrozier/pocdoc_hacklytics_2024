import pandas as pd
import numpy as np

# # Load hospital and patient datasets
# hospital_data = pd.read_csv('hospitalData.csv')
# patient_data = pd.read_csv('hospital_patient_data.csv')

# Function to calculate distance squared between two points
def distance_squared(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

# # Function to assign patients to hospitals based on distance
# def assign_patients_to_hospitals(hospitals, patients):
#     assignments = []
#     for _, patient in patients.iterrows():
#         min_distance = np.inf
#         assigned_hospital = None
#         for _, hospital in hospitals.iterrows():
#             dist_sq = distance_squared(patient['latitudep'], patient['longitudep'], hospital['latitudeh'], hospital['longitudeh'])
#             if dist_sq < min_distance:
#                 min_distance = dist_sq
#                 assigned_hospital = hospital['Hospital']
#         assignments.append((patient['First Name'], patient['Last Name'], assigned_hospital))
#     return assignments

# # Assign patients to hospitals
# patient_assignments = assign_patients_to_hospitals(hospital_data, patient_data)

# # Display patient assignments
# for assignment in patient_assignments:
#     print(f"Patient: {assignment[0]} {assignment[1]} - Assigned Hospital: {assignment[2]}")

import json

# Load hospital and patient datasets
hospital_data = pd.read_csv('HospitalData.csv')
patient_data = pd.read_csv('hospital_patient_data.csv')

# Function to assign patients to hospitals based on distance
def assign_patients_to_hospitals(hospitals, patients):
    assignments = {}
    for _, hospital in hospitals.iterrows():
        hospital_address = hospital['Hospital']
        assignments[hospital_address] = {
            "num_vans": hospital['num_vans'],
            "van_ratio": hospital['van_ratio'],
            "Hospital": []
        }

    for _, patient in patients.iterrows():
        min_distance = np.inf
        assigned_hospital_address = None
        for _, hospital in hospitals.iterrows():
            dist_sq = distance_squared(patient['latitudep'], patient['longitudep'], hospital['latitudeh'], hospital['longitudeh'])
            if dist_sq < min_distance:
                min_distance = dist_sq
                assigned_hospital_address = hospital['Hospital']

        if assigned_hospital_address:
            assignments[assigned_hospital_address]['Hospital'].append({
                "latitude": patient['latitudep'],
                "longitude": patient['longitudep'],
                "escalation": patient['escalation'],
                "first_name": patient['First Name'],
                "last_name": patient['Last Name']
            })

    return assignments

# Assign patients to hospitals
patient_assignments = assign_patients_to_hospitals(hospital_data, patient_data)

# Write to JSON file
with open('hospital_patient_assignments.json', 'w') as json_file:
    json.dump(patient_assignments, json_file, indent=4)
