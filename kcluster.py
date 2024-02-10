import folium
import numpy as np
from sklearn.cluster import KMeans

# Coordinates of {550 Peachtree St NE}
center_latitude = 33.771114
center_longitude = -84.386123

# Given coordinates
coordinates = [
    {"latitude": 33.755671, "longitude": -84.388168},
    {"latitude": 33.785294, "longitude": -84.372491},
    # Add all coordinates here
    {"latitude": 33.750917, "longitude": -84.381309}
]

# Convert coordinates to numpy array
X = np.array([[coord['latitude'], coord['longitude']] for coord in coordinates])

# Number of clusters (adjust as needed)
n_clusters = 5

# Perform KMeans clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X)

# Get cluster centers
cluster_centers = kmeans.cluster_centers_

# Initialize map centered around {550 Peachtree St NE}
mymap = folium.Map(location=[center_latitude, center_longitude], zoom_start=14)

# Add cluster markers to the map
for center in cluster_centers:
    folium.Marker(location=[center[0], center[1]], icon=folium.Icon(color='blue')).add_to(mymap)

# Display the map
mymap.save("cluster_map.html")
