import React, { useEffect, useState } from 'react';
import './SmartDustbinPage.css'; // Import the CSS file
import { Trash, Plus, X } from 'lucide-react'; // Icons for notifications, adding dustbins, and deleting
import axios from 'axios'; // For API requests

const SmartDustbinPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [newDustbin, setNewDustbin] = useState({ location: '', bValue: '', nbValue: '' });

    // Function to fetch dustbin data from backend
    const fetchDustbinData = async () => {
        try {
            const response = await axios.get('http://localhost:5050/api/dustbins');
            setNotifications(response.data);
        } catch (error) {
            console.error('Error fetching dustbin data:', error);
        }
    };

    // Auto-refresh every 5 seconds
    useEffect(() => {
        fetchDustbinData();
        const interval = setInterval(fetchDustbinData, 5000);
        return () => clearInterval(interval);
    }, []);

    // Function to handle report button click
    const handleReport = async (notification) => {
        try {
            const response = await axios.post('http://localhost:5050/api/report', {
                id: notification.id,
                location: notification.location,
                bValue: notification.bValue,
                nbValue: notification.nbValue,
            });

            alert(
                `Server Response: ${response.data.message}\n\n` +
                `Report Details:\n` +
                `ID: ${notification.id}\n` +
                `Location: ${notification.location}\n` +
                `B Value: ${notification.bValue}\n` +
                `NB Value: ${notification.nbValue}`
            );
        } catch (error) {
            console.error('Error sending report:', error.response || error);
            alert('Failed to send report to the server.');
        }
    };

    // Function to handle adding a new dustbin
    const handleAddDustbin = async () => {
        try {
            const response = await axios.post('http://localhost:5050/api/add-dustbin', newDustbin);
            alert(`Dustbin added successfully! ID: ${response.data.dustbin.id}`);
            setNewDustbin({ location: '', bValue: '', nbValue: '' }); // Reset input fields
            fetchDustbinData(); // Refresh the dustbin list
        } catch (error) {
            console.error('Error adding dustbin:', error);
            alert('Failed to add dustbin.');
        }
    };

    // Function to handle deleting a dustbin
    const handleDeleteDustbin = async (id) => {
        try {
            const response = await axios.delete(`http://localhost:5050/api/dustbin/${id}`);
            alert(response.data.message);
            fetchDustbinData(); // Refresh the dustbin list after deletion
        } catch (error) {
            console.error('Error deleting dustbin:', error);
            alert('Failed to delete dustbin.');
        }
    };

    return (
        <div className="smart-dustbin-page">
            <h1>Smart Dustbin Notifications</h1>
            <div className="add-dustbin-section">
                <h2>Add New Dustbin</h2>
                <input
                    type="text"
                    placeholder="Location"
                    value={newDustbin.location}
                    onChange={(e) => setNewDustbin({ ...newDustbin, location: e.target.value })}
                />
                <input
                    type="number"
                    placeholder="B Value"
                    value={newDustbin.bValue}
                    onChange={(e) => setNewDustbin({ ...newDustbin, bValue: e.target.value })}
                />
                <input
                    type="number"
                    placeholder="NB Value"
                    value={newDustbin.nbValue}
                    onChange={(e) => setNewDustbin({ ...newDustbin, nbValue: e.target.value })}
                />
                <button onClick={handleAddDustbin} className="add-dustbin-button">
                    <Plus size={20} /> Add Dustbin
                </button>
            </div>

            <div className="notification-grid">
                {notifications.map((notification) => (
                    <div key={notification.id} className="notification-bar">
                        <div className="notification-icon">
                            <Trash size={24} />
                        </div>
                        <div className="notification-content">
                            <div className="notification-heading">{notification.location}</div>
                            <div className="notification-values">
                                <div className="value-item">
                                    <span className="value-label">B:</span> {notification.bValue}
                                </div>
                                <div className="value-item">
                                    <span className="value-label">NB:</span> {notification.nbValue}
                                </div>
                            </div>
                            <div className="notification-buttons">
                                <button
                                    className="report-button"
                                    onClick={() => handleReport(notification)}
                                >
                                    Report
                                </button>
                                <button
                                    className="delete-button"
                                    onClick={() => handleDeleteDustbin(notification.id)}
                                >
                                    <X size={20} /> Delete
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SmartDustbinPage;
