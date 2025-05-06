import requests   # Lets us send data to a server

import time       # Lets us add time stamps and delays

import random     # Lets us generate fake/random energy numbers



# Our actual VM IP

SERVER_URL = "http://192.168.100.78:5000/api/energy"  # This is where we're sending the data
 

# This function makes fake energy data

def generate_data():

    return {

        "device_id": "raspi01",  # Name or ID of the device (like your Raspberry Pi)

        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # Current date and time

        "energy_consumption": round(random.uniform(1.0, 5.0), 2),  # Random energy use in kWh

        "voltage": round(random.uniform(110.0, 120.0), 1),         # Random voltage value

        "current": round(random.uniform(4.0, 10.0), 2),            # Random current value

    }

 

# This runs forever and keeps sending new data every 10 seconds

while True:

    data = generate_data()  # Make new fake data

    print("Sending:", data)  # Show the data in the terminal

    try:

        response = requests.post(SERVER_URL, json=data)  # Try to send it to the server

        print("Status:", response.status_code, response.text)  # Print server reply

    except Exception as e:

        print("Error sending data:", e)  # If something goes wrong, show the error

    time.sleep(10)  # Wait 10 seconds before doing it again

