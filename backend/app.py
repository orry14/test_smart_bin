from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to communicate with backend

# ✅ Connect to MongoDB
client = MongoClient("mongodb+srv://admin:vq8o0yqH8iZEYj2j@cluster0.bmsri.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["smart_waste_db"]
dustbins_collection = db["dustbin"]

# ✅ API Route to ADD a Dustbin
@app.route("/api/add-dustbin", methods=["POST"])
def add_dustbin():
    try:
        data = request.json
        location = data.get("location")
        b_value = data.get("bValue")
        nb_value = data.get("nbValue")

        if not location or b_value is None or nb_value is None:
            return jsonify({"error": "Missing data"}), 400

        # Insert into MongoDB
        dustbins_collection.insert_one({
            "location": location,
            "bValue": b_value,
            "nbValue": nb_value
        })

        return jsonify({"message": "Dustbin added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API Route to GET all Dustbins
@app.route("/api/dustbins", methods=["GET"])
def get_dustbins():
    dustbins = list(dustbins_collection.find({}, {"_id": 0}))  # Hide _id field
    return jsonify(dustbins), 200

# ✅ API Route to DELETE a Dustbin by Location
@app.route("/api/delete-dustbin", methods=["DELETE"])
def delete_dustbin():
    try:
        data = request.json
        location = data.get("location")

        if not location:
            return jsonify({"error": "Location required"}), 400

        result = dustbins_collection.delete_one({"location": location})
        if result.deleted_count == 0:
            return jsonify({"error": "Dustbin not found"}), 404

        return jsonify({"message": "Dustbin deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API Route to UPDATE a Dustbin's Fill Level
@app.route("/api/update-dustbin", methods=["PUT"])
def update_dustbin():
    try:
        data = request.json
        location = data.get("location")
        b_value = data.get("bValue")
        nb_value = data.get("nbValue")

        if not location or b_value is None or nb_value is None:
            return jsonify({"error": "Missing data"}), 400

        result = dustbins_collection.update_one(
            {"location": location},
            {"$set": {"bValue": b_value, "nbValue": nb_value}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Dustbin not found"}), 404

        return jsonify({"message": "Dustbin updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run the Flask Server
if __name__ == "__main__":
    app.run(debug=True, port=5050)
