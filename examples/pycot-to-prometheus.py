import json
import time

from prometheus_client import Gauge, start_http_server

# Load your JSON data
with open("your_data.json", "r") as file:
    data = json.load(file)

# Define your metrics
lat_metric = Gauge("latitude", "Latitude of the location", ["location"])
lon_metric = Gauge("longitude", "Longitude of the location", ["location"])


def process_data():
    for location, coords in data.items():
        lat_metric.labels(location=location).set(coords["lat"])
        lon_metric.labels(location=location).set(coords["lon"])


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Update the metrics with your data
    while True:
        process_data()
        time.sleep(15)
