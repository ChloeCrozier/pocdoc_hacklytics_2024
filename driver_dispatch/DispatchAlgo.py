import json
import numpy as np
from sklearn.cluster import KMeans

# Load data from JSON file
with open('patients_by_hospital(3).json', 'r') as file:
    data = json.load(file)

# Extract patient locations
patient_locations = []
for hospital in data['hospitals'].values():
    for patient in hospital['patients']:
        patient_locations.append([patient['latitude'], patient['longitude']])

# Convert to numpy array
patient_locations = np.array(patient_locations)

# Initialize and fit KMeans model with random initialization
kmeans = KMeans(n_clusters=25, init='random', n_init=10)  # Specify the number of clusters and number of initializations
kmeans.fit(patient_locations)

# Get cluster centroids and labels
centroids = kmeans.cluster_centers_
labels = kmeans.labels_

# Print cluster centroids and labels
print("Cluster Centroids:")
for i, centroid in enumerate(centroids):
    print(f"Cluster {i+1}: {centroid}")

print("Labels:")
print(labels)
