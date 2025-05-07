from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def update_appliance_status(appliance, status):
    conn = sqlite3.connect("smart_home.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE appliances SET status = ? WHERE name = ?", (status, appliance))
    conn.commit()
    conn.close()

@app.route("/control-appliance", methods=["POST"])
def control_appliance():
    data = request.get_json()
    appliance = data.get("appliance")
    action = data.get("action")

    if appliance and action in ["on", "off"]:
        update_appliance_status(appliance, action)
        return jsonify({"status": "success", "appliance": appliance, "action": action})

    return jsonify({"status": "error", "message": "Invalid request"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
