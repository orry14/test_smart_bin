from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId for serialization

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['smart_dustbin_db']
reports_collection = db['reports']
dustbins_collection = db['dustbins']

# Helper function to serialize ObjectId
def serialize_document(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Endpoint to receive reports
@app.route('/api/report', methods=['POST'])
def receive_report():
    data = request.json
    if not all(k in data for k in ('id', 'location', 'bValue', 'nbValue')):
        return jsonify({"message": "Invalid report data!"}), 400
    result = reports_collection.insert_one(data)
    data['_id'] = str(result.inserted_id)  # Convert ObjectId to string for JSON response
    print(f"Received Report: {data}")
    return jsonify({"message": "Report received successfully!", "report": data}), 201

# Endpoint to fetch all reports
@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = list(reports_collection.find({}))
    serialized_reports = [serialize_document(report) for report in reports]
    return jsonify(serialized_reports), 200

# Endpoint to mark a report as completed
@app.route('/api/complete', methods=['POST'])
def complete_report():
    data = request.json
    report_id = data.get('id')
    if not report_id:
        return jsonify({"message": "Report ID is required!"}), 400
    result = reports_collection.delete_one({'id': report_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Report not found!"}), 404
    updated_reports = list(reports_collection.find({}))
    serialized_reports = [serialize_document(report) for report in updated_reports]
    return jsonify({"message": "Report marked as completed!", "updated_reports": serialized_reports}), 200

# Endpoint to add a new dustbin
@app.route('/api/add-dustbin', methods=['POST'])
def add_dustbin():
    data = request.json
    if not all(k in data for k in ('location', 'bValue', 'nbValue')):
        return jsonify({"message": "Invalid dustbin data!"}), 400
    new_dustbin = {
        "id": dustbins_collection.count_documents({}) + 1,
        "location": data.get('location'),
        "bValue": data.get('bValue'),
        "nbValue": data.get('nbValue')
    }
    result = dustbins_collection.insert_one(new_dustbin)
    new_dustbin["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    print(f"Added new dustbin: {new_dustbin}")
    return jsonify({"message": "Dustbin added successfully!", "dustbin": new_dustbin}), 201

# Endpoint to fetch all dustbins
@app.route('/api/dustbins', methods=['GET'])
def get_dustbins():
    dustbins = list(dustbins_collection.find({}))
    serialized_dustbins = [serialize_document(dustbin) for dustbin in dustbins]
    return jsonify(serialized_dustbins), 200
@app.route('/api/reset-dustbin', methods=['POST'])
def reset_dustbin():
    data = request.json
    dustbin_id = data.get('id')
    
    if not dustbin_id:
        return jsonify({"message": "Dustbin ID is required!"}), 400
    
    # Reset the dustbin values to 0
    result = dustbins_collection.update_one(
        {"id": dustbin_id},
        {"$set": {"bValue": 0, "nbValue": 0}}
    )
    
    if result.matched_count == 0:
        return jsonify({"message": "Dustbin not found!"}), 404
    
    # Delete the corresponding report from the reports collection
    reports_collection.delete_many({"id": dustbin_id})
    
    return jsonify({"message": "Dustbin values reset and corresponding report deleted successfully!"}), 200

# Endpoint to display full content in DB
@app.route('/api/db-content', methods=['GET'])
def get_db_content():
    reports = list(reports_collection.find({}))
    dustbins = list(dustbins_collection.find({}))
    serialized_reports = [serialize_document(report) for report in reports]
    serialized_dustbins = [serialize_document(dustbin) for dustbin in dustbins]
    return jsonify({"reports": serialized_reports, "dustbins": serialized_dustbins}), 200
# Endpoint to delete a dustbin
@app.route('/api/dustbin/<int:id>', methods=['DELETE'])
def delete_dustbin(id):
    result = dustbins_collection.delete_one({'id': id})
    if result.deleted_count == 0:
        return jsonify({"message": "Dustbin not found!"}), 404
    return jsonify({"message": "Dustbin deleted successfully!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

