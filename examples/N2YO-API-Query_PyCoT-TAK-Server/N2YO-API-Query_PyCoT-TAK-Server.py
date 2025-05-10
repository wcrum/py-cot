import CoT  # https://pypi.org/project/PyCoT
import requests
import datetime
import socket
import ssl
import time
import os
import logging

# Configure logging to track script activity
# Logs are saved to a file for debugging and monitoring
logging.basicConfig(
    filename="/home/luke_blue_lox/PycharmProjects/BLOX-TAK-CoT/cot.log",  # Path to the log file
    level=logging.INFO,  # Log level (INFO and above)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format: timestamp, level, message
)

# https://www.n2yo.com/api
N2YO_API_KEY = "**********"  # Replace with your N2YO API key (get it from n2yo.com)
SAT_ID = 6073  # Satellite ID for COSMOS 482 DESCENT CRAFT (NORAD ID)
OBSERVER_LAT = 50.81557  # Observer's latitude (your location, in degrees)
OBSERVER_LNG = 15.675225  # Observer's longitude (your location, in degrees)
OBSERVER_ALT = 445  # Observer's altitude above sea level (in meters)
SECONDS = 1  # Number of seconds of position data to fetch from N2YO (1 position in this case)
REFRESH_INTERVAL = 10  # Delay between CoT messages (in seconds), controls how often the marker updates in TAK

# TAK server settings for sending CoT messages
TAK_IP = "192.168.1.17"  # IP address of the TAK erver
TAK_PORT = 8089  # SSL port for TAK server (default for SSL connections)

# Paths to SSL certificates for secure connection to the TAK server
CERT_DIR = "/home/luke_blue_lox/PycharmProjects/BLOX-TAK-CoT/certs"  # Directory containing certificates
CLIENT_CERT = os.path.join(CERT_DIR, "LukeBlueLOx.pem")  # Client certificate (PEM format)
CLIENT_KEY = os.path.join(CERT_DIR, "LukeBlueLOx.key")  # Client private key (PEM format)
CA_CERT = os.path.join(CERT_DIR, "truststore-root.pem")  # CA certificate for server verification

# Configure SSL context for secure communication with the TAK server
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Use TLS client protocol
ssl_context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)  # Load client cert and key
ssl_context.load_verify_locations(cafile=CA_CERT)  # Load CA cert to verify the server
ssl_context.verify_mode = ssl.CERT_REQUIRED  # Require server certificate verification

# Main loop: continuously fetch satellite positions and send CoT messages to TAK
while True:
    try:
        # Fetch satellite position from N2YO API
        start_time = time.time()  # Record start time to measure query duration
        url = f"https://api.n2yo.com/rest/v1/satellite/positions/{SAT_ID}/{OBSERVER_LAT}/{OBSERVER_LNG}/{OBSERVER_ALT}/{SECONDS}/&apiKey={N2YO_API_KEY}"
        response = requests.get(url)  # Send HTTP GET request to N2YO API
        query_time = time.time() - start_time  # Calculate how long the query took

        # Check if the API request was successful
        if response.status_code != 200:
            error_message = f"N2YO API Error: {response.status_code} - {response.text}"
            print(error_message)
            logging.error(error_message)
            time.sleep(60)  # Wait 60 seconds before retrying (to avoid hitting API limits)
            continue

        # Parse the API response
        data = response.json()
        positions = data.get("positions", [])  # Extract position data (list of positions)
        if not positions:
            error_message = "No positions returned from N2YO"
            print(error_message)
            logging.error(error_message)
            time.sleep(60)  # Wait 60 seconds before retrying
            continue

        # Extract satellite name and log the number of positions fetched
        sat_name = data["info"]["satname"]  # Get satellite name (e.g., "COSMOS 482 DESCENT CRAFT")
        remaining = response.headers.get("X-Rate-Limit-Remaining", "Unknown")  # Get remaining API quota
        log_message = f"Fetched {len(positions)} positions for {sat_name}, query took {query_time:.2f} seconds, API limit remaining: {remaining}"
        print(log_message)
        logging.info(log_message)

        # Establish a secure connection to the TAK server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        wrapped_sock = ssl_context.wrap_socket(sock, server_hostname=TAK_IP)  # Wrap socket with SSL
        wrapped_sock.connect((TAK_IP, TAK_PORT))  # Connect to the TAK server
        wrapped_sock.settimeout(1)  # Set a 1-second timeout for receiving responses

        # Process each position and send a CoT message to the TAK server
        for sat_data in positions:
            # Extract satellite position data
            sat_lat = sat_data["satlatitude"]  # Latitude in degrees
            sat_lon = sat_data["satlongitude"]  # Longitude in degrees
            sat_alt = sat_data["sataltitude"] * 1000  # Altitude in meters (convert from kilometers)

            # Set timestamps for the CoT message
            now = datetime.datetime.now(datetime.timezone.utc)  # Current time in UTC
            stale = now + datetime.timedelta(minutes=5)  # Set expiration time (5 minutes from now)

            # Create a CoT event for the satellite position
            cot_event = CoT.Event(
                version="2.0",  # CoT protocol version
                type="a-n-G-U-U-S-R-S",  # CoT type: https://github.com/wcrum/py-cot/blob/main/CoT/types.py
                access="Undefined",  # Access level (optional)
                uid=f"SAT.{SAT_ID}",  # Unique identifier for the satellite (e.g., "SAT.6073")
                time=now,  # Time of the event
                start=now,  # Start time of the event
                stale=stale,  # Expiration time of the event
                how="m-g",  # How the data was obtained (machine-generated)
                qos="2-i-c",  # Quality of service: informational, continuous
                point=CoT.Point(
                    lat=sat_lat,  # Latitude
                    lon=sat_lon,  # Longitude
                    hae=sat_alt,  # Height above ellipsoid (altitude in meters)
                    ce=9999999,  # Circular error (unknown, max value)
                    le=9999999  # Linear error (unknown, max value)
                ),
                detail={"contact": {"callsign": sat_name}}  # Additional details (satellite name as callsign)
            )

            # Send the CoT message to the TAK server
            wrapped_sock.sendall(bytes(cot_event.xml(), encoding="utf-8"))  # Convert CoT to XML and send

            # Log the position data
            position_message = f"CoT for {sat_name}: lat={sat_lat}, lon={sat_lon}, alt={sat_alt}"
            print(position_message)
            logging.info(position_message)

            # Try to receive a response from the TAK server
            try:
                response = wrapped_sock.recv(1024).decode("utf-8")  # Receive up to 1024 bytes
                log_message = f"Sent SSL CoT for {sat_name} to {TAK_IP}:{TAK_PORT}, Response: {response}"
            except socket.timeout:
                log_message = f"Sent SSL CoT for {sat_name} to {TAK_IP}:{TAK_PORT}, No response"
            print(log_message)
            logging.info(log_message)

            # Wait before sending the next CoT message
            time.sleep(REFRESH_INTERVAL)  # Delay between updates (10 seconds)

        # Close the connection to the TAK server
        wrapped_sock.close()

    except requests.RequestException as e:
        # Handle errors related to the N2YO API request
        error_message = f"N2YO API request error: {e}"
        print(error_message)
        logging.error(error_message)
    except (ConnectionRefusedError, ssl.SSLError) as e:
        # Handle SSL or connection errors with the TAK server
        error_message = f"SSL connection error to TAK server: {e}"
        print(error_message)
        logging.error(error_message)
    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"Unexpected error: {e}"
        print(error_message)
        logging.error(error_message)
