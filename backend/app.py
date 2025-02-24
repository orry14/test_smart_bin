from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from ultralytics import YOLO
import cv2
import numpy as np
import os
import time
from scipy.optimize import linear_sum_assignment

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['smart_dustbin_db']
reports_collection = db['reports']
dustbins_collection = db['dustbins']

# Load YOLO models
pose_model = YOLO('yolo11n-pose.pt')  # Pose estimation model
trash_model = YOLO('best.pt')  # Trained trash detection model

# Setup screenshot directory
screenshot_folder = 'static/screenshots'
os.makedirs(screenshot_folder, exist_ok=True)
screenshot_counter = 0

# Detection parameters
DISTANCE_THRESHOLD = 200
VELOCITY_THRESHOLD = 20
VELOCITY_SMOOTHING_WINDOW = 5
velocity_buffer = []
previous_trash_centers = []

# Helper function to serialize ObjectId
def serialize_document(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Smooth velocity function
def smooth_velocity(velocity, window_size=VELOCITY_SMOOTHING_WINDOW):
    velocity_buffer.append(velocity)
    if len(velocity_buffer) > window_size:
        velocity_buffer.pop(0)
    return np.mean(velocity_buffer)

# Video stream and litter detection
def generate_frames():
    global screenshot_counter, previous_trash_centers
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Camera not accessible."

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        pose_results = pose_model(frame, conf=0.5)
        annotated_frame = pose_results[0].plot(show=False)

        keypoints = pose_results[0].keypoints[0]
        left_hand = right_hand = None
        for i in range(len(keypoints.xy[0])):
            x, y = keypoints.xy[0][i]
            confidence = keypoints.conf[0][i]
            if confidence > 0.4:
                if i == 9:
                    left_hand = (int(x), int(y))
                elif i == 10:
                    right_hand = (int(x), int(y))

        trash_results = trash_model(frame)
        current_trash_centers = []
        for result in trash_results:
            if result.boxes is not None:
                for box in result.boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    if conf > 0.5:
                        class_names = ['bio', 'non-bio', 'residual']
                        class_name = class_names[cls]
                        x1, y1, x2, y2 = map(int, xyxy)
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(annotated_frame, f"{class_name}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                        current_trash_centers.append((center_x, center_y))

        if left_hand and right_hand:
            for center_x, center_y in current_trash_centers:
                left_distance = np.linalg.norm(np.array([center_x, center_y]) - np.array(left_hand))
                right_distance = np.linalg.norm(np.array([center_x, center_y]) - np.array(right_hand))
                cost_matrix = np.array([[left_distance], [right_distance]])
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                if cost_matrix[row_ind, col_ind] < DISTANCE_THRESHOLD:
                    if previous_trash_centers:
                        prev_center = previous_trash_centers[-1]
                        velocity = np.linalg.norm(np.array([center_x, center_y]) - np.array(prev_center))
                        smoothed_velocity = smooth_velocity(velocity)
                        if smoothed_velocity > VELOCITY_THRESHOLD:
                            cv2.putText(annotated_frame, "Trash Thrown", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            screenshot_path = os.path.join(screenshot_folder, f"throw_{screenshot_counter}.png")
                            cv2.imwrite(screenshot_path, annotated_frame)
                            screenshot_counter += 1
        previous_trash_centers = current_trash_centers

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Routes
@app.route('/')
def index():
    return "Litter Detection System Running"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/screenshots', methods=['GET'])
def get_screenshots():
    search_query = request.args.get('query', '').lower()  # Get the search query from request parameters
    images = os.listdir(screenshot_folder)
    # Filter images based on the search query
    filtered_images = [f"/static/screenshots/{img}" for img in images if search_query in img.lower()]
    return jsonify(filtered_images)

@app.route('/api/dustbin/<int:dustbin_id>', methods=['DELETE'])
def delete_dustbin(dustbin_id):
    result = dustbins_collection.delete_one({'id': dustbin_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Dustbin not found!"}), 404
    return jsonify({"message": "Dustbin deleted successfully!"}), 200

@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    return send_from_directory(screenshot_folder, filename)

# MongoDB operations for reports and dustbins
@app.route('/api/report', methods=['POST'])
def receive_report():
    data = request.json
    if not all(k in data for k in ('id', 'location', 'bValue', 'nbValue')):
        return jsonify({"message": "Invalid report data!"}), 400
    result = reports_collection.insert_one(data)
    data['_id'] = str(result.inserted_id)
    return jsonify({"message": "Report received successfully!", "report": data}), 201

@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = list(reports_collection.find({}))
    serialized_reports = [serialize_document(report) for report in reports]
    return jsonify(serialized_reports), 200

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
    new_dustbin["_id"] = str(result.inserted_id)
    return jsonify({"message": "Dustbin added successfully!", "dustbin": new_dustbin}), 201

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
    result = dustbins_collection.update_one(
        {"id": dustbin_id},
        {"$set": {"bValue": 0, "nbValue": 0}}
    )
    if result.matched_count == 0:
        return jsonify({"message": "Dustbin not found!"}), 404
    reports_collection.delete_many({"id": dustbin_id})
    return jsonify({"message": "Dustbin values reset and corresponding reports deleted successfully!"}), 200

@app.route('/api/db-content', methods=['GET'])
def get_db_content():
    reports = list(reports_collection.find({}))
    dustbins = list(dustbins_collection.find({}))
    serialized_reports = [serialize_document(report) for report in reports]
    serialized_dustbins = [serialize_document(dustbin) for dustbin in dustbins]
    return jsonify({"reports": serialized_reports, "dustbins": serialized_dustbins}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
