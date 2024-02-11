#!/usr/bin/env python3
import json
from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial import distance

def assign_vans_to_hospitals(input_json, output_json):
    # Load JSON data
    with open(input_json, 'r') as f:
        data = json.load(f)

    hospitals = data['hospitals']
    assigned_units = {}

    # Iterate over hospitals
    for hospital, details in hospitals.items():
        num_vans = details.get('num_vans', 0)
        patients = details.get('patients', [])
        longitude = details.get('longitude', 0)
        latitude = details.get('latitude', 0)
        address = details.get('address', '')

        if num_vans > 0 and len(patients) > 0:
            # Extract patient coordinates
            patient_coords = np.array([[patient['latitude'], patient['longitude']] for patient in patients])

            # Perform k-means clustering
            kmeans = KMeans(n_clusters=int(num_vans), random_state=42).fit(patient_coords)
            cluster_centers = kmeans.cluster_centers_

            # Create units based on cluster centers
            units = [{"unit_name": f"unit{i + 1}", "latitude": center[0], "longitude": center[1], "patients": []}
                     for i, center in enumerate(cluster_centers)]

            # Assign each patient to the nearest unit
            for patient in patients:
                patient_coord = np.array([patient['latitude'], patient['longitude']])
                distances = [distance.euclidean(patient_coord, center) for center in cluster_centers]
                nearest_unit_index = np.argmin(distances)
                units[nearest_unit_index]['patients'].append(patient)

            assigned_units[hospital] = {
                "num_vans": num_vans,
                "facility_name": details.get("facility_name", hospital),
                "longitude": longitude,
                "latitude": latitude,
                "address": address,
                "units": units
            }
        else:
            assigned_units[hospital] = {
                "num_vans": 0,
                "facility_name": details.get("facility_name", hospital),
                "longitude": longitude,
                "latitude": latitude,
                "address": address,
                "units": []
            }

    # Wrap assigned units into a "hospitals" key
    output_data = {"hospitals": assigned_units}

    # Write assigned units to output JSON file
    with open(output_json, 'w') as f:
        json.dump(output_data, f, indent=4)

# Input and output file paths
input_json = 'patients_by_hospital.json'
output_json = 'assigned_units.json'

# Assign vans to hospitals
assign_vans_to_hospitals(input_json, output_json)

print("Vans assigned to hospitals. Results saved to assigned_units.json.")
