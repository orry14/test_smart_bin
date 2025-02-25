# ♻️ Zero-Waste Smart Management System

## 🌐 Project Overview
This project is an AI-powered smart waste management system designed to promote responsible waste disposal and enhance urban sanitation. It integrates litter detection, smart dustbins, and automated waste processing to optimize waste collection and promote sustainability.

## 🚀 Features
- 🎥 **AI-Powered Litter Detection:** Detects littering in real-time using CCTV and facial recognition.  
- 📲 **Aadhaar-Linked Penalty System:** Issues penalties automatically by identifying offenders through Aadhaar data.  
- 🗑️ **Smart Waste Segregation:** Automatically classifies waste as biodegradable or non-biodegradable using computer vision.  
- 📡 **Real-Time Monitoring:** Tracks dustbin fill levels with ultrasonic sensors and sends alerts.  
- 🔄 **Automated Waste Processing:** Converts biodegradable waste into methane and organic fertilizers.  
- 🧲 **Magnetic Sorting System:** Separates recyclable non-biodegradable materials.  

## 🏗️ Tech Stack
- **Frontend:** React.js, Tailwind CSS  
- **Backend:** Flask (Python)  
- **Machine Learning Libraries:** TensorFlow, PyTorch, OpenCV, NumPy, Pandas  
- **Database:** SQLite / MySQL (based on project requirements)  
- **Other Tools:** Ultrasonic sensors, CCTV surveillance, Magnetic conveyor systems  

## ⚙️ Installation Guide

### Prerequisites
- Node.js and npm (for React)
- Python 3.x and pip (for Flask)
- Virtual environment (recommended for Python)

### Backend Setup (Flask)
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup (React)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install React dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## 📱 Usage Instructions
1. Launch both the backend (Flask) and frontend (React) servers.  
2. Access the web application at `http://localhost:3000/`.  
3. Use the **Waste Throwing Detect** page for real-time litter detection.  
4. Monitor dustbin status on the **Smart Dustbin** page.  
5. View waste processing updates on the **Automated Recycling** page.  

## 📊 System Workflow
1. Detects littering incidents via CCTV and issues penalties automatically.  
2. Smart dustbins classify waste and monitor fill levels.  
3. Real-time alerts are sent to municipal cleaners when bins are full.  
4. Waste is processed for energy generation and recycling.  

## 🤝 Contributors
- Krishna Prasad
- Sudhin Suresh
- Aasish S

## 📜 License
This project is licensed under the [MIT License](LICENSE).

## 📧 Contact
For queries, contact us at [krishnaprasadsm63@gmail.com].