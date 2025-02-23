from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Storage for reports
reports = []

@app.route('/api/report', methods=['POST'])
def receive_report():
    data = request.json
    reports.append(data)  # Store the report in-memory
    print(f"Received Report: {data}")
    return jsonify({"message": "Report received successfully!"})

@app.route('/api/reports', methods=['GET'])
def get_reports():
    return jsonify(reports)

@app.route('/api/complete', methods=['POST'])
def complete_report():
    data = request.json
    for report in reports:
        if report['id'] == data['id']:
            report['bValue'] = "0%"
            report['nbValue'] = "0%"
    return jsonify({"message": "Report marked as completed!"})

if __name__ == '__main__':
    app.run(port=5050)
