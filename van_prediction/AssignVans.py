import json
from pulp import LpProblem, LpVariable, lpSum, LpMaximize

# Read data from JSON file
with open('test.json') as f:
    data = json.load(f)

hospitals_data = data.get('hospitals', {})

# Extract relevant data from JSON
hospitals = list(hospitals_data.keys())
patients = [len(hospitals_data[hospital].get('patients', [])) for hospital in hospitals]
escalation_rate = [sum(patient.get('escalation', 0) for patient in hospitals_data[hospital].get('patients', [])) / max(len(hospitals_data[hospital].get('patients', [])), 1) for hospital in hospitals]

# Other parameters
num_hospitals = len(hospitals)
total_vans_available = 25
minimum_vans_per_hospital = 2  # Example minimum vans per hospital, replace with actual data
weights_patients = 1  # Weight for number of patients
weights_escalation = 2  # Weight for average escalation rate

# Define the linear optimization problem
prob = LpProblem("HospitalVansAllocation", LpMaximize)

# Define decision variables
x = [LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(1, num_hospitals + 1)]

# Define objective function
prob += lpSum((patients[i] * weights_patients + escalation_rate[i] * weights_escalation) * x[i] for i in range(num_hospitals))

# Define constraints
prob += lpSum(x) <= total_vans_available, "TotalVansConstraint"
for i in range(num_hospitals):
    if patients[i] == 0:
        prob += x[i] == 0  # Set 1 van for hospitals with no patients
    else:
        prob += x[i] >= minimum_vans_per_hospital, f"MinVansHospital{i+1}"

# Solve the problem
prob.solve()

# Output the results
print("Status:", prob.status)
print("Optimal allocation of vans to hospitals:")
for i in range(num_hospitals):
    print(f"{hospitals[i]}: {x[i].varValue} vans")

print("Total number of vans allocated:", sum(x[i].varValue for i in range(num_hospitals)))
