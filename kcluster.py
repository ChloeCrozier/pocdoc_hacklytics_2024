#!/usr/bin/env python3
import numpy as np
from sklearn.cluster import KMeans
from mapboxgl.viz import CircleViz
from IPython.display import HTML, display

# Given addresses with escalation levels
addresses = [
    {"latitude": 33.755671, "longitude": -84.388168, "escalation": 2},
    {"latitude": 33.785294, "longitude": -84.372491, "escalation": 3},
    {"latitude": 33.767912, "longitude": -84.360572, "escalation": 2},
    # Add all addresses with escalation levels here
]

# Convert addresses to numpy array
X = np.array([[address['longitude'], address['latitude']] for address in addresses])

# Number of clusters
n_clusters = 5

# Perform KMeans clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X)

# Get cluster centers
cluster_centers = kmeans.cluster_centers_

# Create GeoJSON data
features = []
for center in cluster_centers:
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [center[0], center[1]]
        },
        "properties": {
            "marker-color": "#ff0000",
            "marker-symbol": "marker"
        }
    })

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Create a Mapbox map
viz = CircleViz(
    geojson_data,
    access_token='YOUR_MAPBOX_ACCESS_TOKEN',
    color_property='marker-color',
    color_stops=[
        [0, '#00ff00'],  # green
        [1, '#ff0000']   # red
    ],
    radius=10,
    center=(addresses[0]['longitude'], addresses[0]['latitude']),
    zoom=10
)

viz.show()