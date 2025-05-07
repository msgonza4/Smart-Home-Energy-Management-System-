from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/control-appliance", methods=["POST"])
def control_appliance():
    data = request.get_json()
    action = data.get("action")

    if action == "on":
        print("Appliance turned ON")
    elif action == "off":
        print("Appliance turned OFF")

    return jsonify({"status": "success", "action": action})
if __name__ == "__main__":
   app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) 
