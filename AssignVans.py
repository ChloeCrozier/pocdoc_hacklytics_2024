import json
import numpy as np

# Load the JSON data from file
with open('hospital_patient_assignments.json', 'r') as file:
    data = json.load(file)

# Initialize a list to store hospital scores
hospital_scores = []

# Define weights for each factor
weights = {
    "median_wait_time": 0.3,
    "county_population": 0.2,
    "avg_healthcare_case_severity": 0.3,
    "num_patients_near_hospital": 0.2
}

# Iterate over each hospital in the data
for address, hospital_info in data.items():
    hospital_data = hospital_info.get("Hospital", [])
    if hospital_data:
        # Initialize variables for scoring
        score = 0
        total_weight = 0

        # Iterate over each hospital data
        for hospital in hospital_data:
            # Calculate weighted score for each factor
            for factor, weight in weights.items():
                score += hospital.get(factor, 0) * weight
                total_weight += weight

        # Normalize the score
        normalized_score = score / total_weight

        # Append hospital address and normalized score to the list
        hospital_scores.append((address, normalized_score))

# Sort hospitals by their scores
hospital_scores.sort(key=lambda x: x[1], reverse=True)

# Initialize dictionary to store vans distribution
hospital_vans = {address: 0 for address, _ in hospital_scores}

# Distribute vans to hospitals until all 50 vans are allocated
remaining_vans = 50
for address, _ in hospital_scores:
    vans_for_hospital = min(int(remaining_vans / len(hospital_scores)), remaining_vans)
    hospital_vans[address] += vans_for_hospital
    remaining_vans -= vans_for_hospital
    if remaining_vans == 0:
        break

# Print the distribution of vans for each hospital
for address, vans in hospital_vans.items():
    print(f"Hospital: {address}, Vans: {vans}")

