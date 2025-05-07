import requests

def fetch_data_from_pi(pi_ip):
    try:
        response = requests.get(f"http://{pi_ip}:5000/data")
        data = response.json()
        return data
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

pi_ip = "192.168.100.78"  # Your Flask server (VirtualBox) IP


def create_graph(data, max_width=50):
    max_val = max(data.values())

    for label, value in data.items():
        #scales to fit max width of terminal
        num_blocks = int((value / max_val) * max_width)
        bar = '█' * num_blocks
        print(f"{label}: {bar} ({value})")


while True:
    data = fetch_data_from_pi(pi_ip)
    if data is None:
        print("Data not found")
        continue

    #  Assign values from Flask response
    latest0 = data[0]
    latest1 = data[1]
    latest2 = data[2]
    
    energycon0 = latest0["energy_consumption"]
    energycon1 = latest1["energy_consumption"]
    energycon2 = latest2["energy_consumption"]

    timestamp = latest1["timestamp"]
    voltage = latest1["voltage"]
    current = latest1["current"]

    comd = float(input(
        "Home Energy Management System.\n"
        "1. energy consumption\n"  
        "1.5. make graph of last 3 energy #'s\n"
        "2. voltage\n"
        "3. current\n"
        "4. quit\n"
    ))

    if comd == 1:
        print(f"{timestamp}: {energycon0} kWh\n")
    elif comd == 1.5:
        graph_data = {
        "Energy log 0 (kWh)": energycon0,
        "Energy log 1 (kWh)": energycon1,
        "Energy log 2 (kWh)": energycon2
        }

        create_graph(graph_data)
    elif comd == 2:
        print(f"{timestamp}: {voltage} V\n")
    elif comd == 3:
        print(f"{timestamp}: {current} A\n")
    elif comd == 4:
        print("See you next time!")
        break
    else:
        print("Invalid response. Try again.")