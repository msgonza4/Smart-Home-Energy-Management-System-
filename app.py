from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
DATABASE = 'energy.db'

# Home route for browser access
@app.route('/')
def home():
    return "<h1>Smart Home Energy Server is Running</h1><p>Use /api/energy to POST or GET data.</p>"

#@app.route('/data')
#def get_data():
 #   data = {
  #      "timestamp": datetime.now().strftime("%H:%M:%S"),
   #     "kWh": round(random.uniform(100.0, 300.0), 2),
    #    "voltage": round(random.uniform(210.0, 250.0), 2),
     #   "current": round(random.uniform(2.0, 10.0), 2)
  #  }
  # return jsonify(data)

#gael- i commenteed the above out because functions cant have the same app route and this function wasnt necessary for what we are doing

# Helper: Insert data
def insert_energy_data(timestamp, device_id, energy, voltage, current):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO energy_data (timestamp, device_id, energy_consumption, voltage, current) VALUES (?, ?, ?, ?, ?)",
              (timestamp, device_id, energy, voltage, current))
    conn.commit()
    conn.close()

# POST endpoint to insert data
@app.route('/api/energy', methods=['POST'])
def add_energy_data():
    data = request.get_json()
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())  #gael- i think u should change the timestamp from the system timestamp to the timestamp variable sent from terrels pi
    device_id = data['device_id']
    energy = data['energy_consumption']
    voltage = data['voltage']
    current = data['current']
   
    insert_energy_data(timestamp, device_id, energy, voltage, current)
    return jsonify({"message": "Data inserted successfully"}), 201

# Helper: Retrieve data
def get_energy_data(start=None, end=None):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if start and end:
        c.execute("SELECT * FROM energy_data WHERE timestamp BETWEEN ? AND ?", (start, end))
    else:
        c.execute("SELECT * FROM energy_data")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/api/dashboard')
def api_dashboard():
    data = get_energy_data()  # Assuming this is the helper function fetching data from SQLite DB
    result = [
        {
            "id": row[0],
            "timestamp": row[1],
            "device_id": row[2],
            "energy_consumption": row[3],
            "voltage": row[4],
            "current": row[5]
        }
        for row in data
    ]
    return jsonify(result)

# GET endpoint to retrieve data (optionally filtered by timestamp)
@app.route('/api/energy', methods=['GET'])
def get_energy():
    start = request.args.get('start')
    end = request.args.get('end')
    data = get_energy_data(start, end)
    result = [
        {"id": row[0], "timestamp": row[1], "device_id": row[2], "energy_consumption": row[3], "voltage": row[4], "current": row[5]}
        for row in data
    ]
    return jsonify(result)
    
@app.route('/data', methods=['GET'])
def get_latest_data():
    device_id = request.args.get('device_id', 'raspi01')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM energy_data WHERE device_id = ? ORDER BY timestamp DESC LIMIT 3", ('raspi01',))
    
    rows = c.fetchall()
    conn.close()

    if rows:
        result = [
        {
            "id": row[0],
            "timestamp": row[1],
            "device_id": row[2],
            "energy_consumption": row[3],
            "voltage": row[4],
            "current": row[5]
        }
        for row in rows
   	]
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404

#@app.route('/data')
#def data():
    # Replace with live sensor reading or simulated update
   # return jsonify({
       # "timestamp": datetime.utcnow().isoformat(),
      #  "kWh": random.uniform(10.0, 100.0),
     #   "voltage": random.uniform(110, 120),
    #    "current": random.uniform(5, 10)
   # })

#gael- i commented this stuff out too because it looked like a copy of the first function i commented out


@app.route('/dashboard')
def dashboard():
    data = get_energy_data()
    html = "<h2>Stored Energy Data</h2><table border='1'>"
    html += "<tr><th>ID</th><th>Timestamp</th><th>Device ID</th><th>Energy</th><th>Voltage</th><th>Current</th></tr>"
    for row in data:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
    html += "</table>"
    return html
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
