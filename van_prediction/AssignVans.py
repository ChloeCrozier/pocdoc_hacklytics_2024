import json

# Load the JSON data from file
with open('patients_by_hospital.json', 'r') as file:
    data = json.load(file)

# Initialize a list to store hospital scores
hospital_scores = []

# Define weights for each factor
weights = {
    "median_wait_time": 0.3,
    "county_population_density": 0.2,
    "avg_healthcare_case_severity": 0.3,
    "num_patients_near_hospital": 0.2
}

# Iterate over each hospital in the data
for address, hospital_info in data["hospitals"].items():
    hospital_data = hospital_info.get("patients", [])
    if hospital_data:
        # Initialize variables for scoring
        score = 0

        # Iterate over each hospital data
        for patient in hospital_data:
            # Calculate weighted score for each factor
            for factor, weight in weights.items():
                score += patient.get(factor, 0) * weight

        # Update num_vans field directly in the JSON
        hospital_info["num_vans"] = score

# Save the updated JSON back to the file
with open('patients_by_hospital.json', 'w') as file:
    json.dump(data, file, indent=4)
