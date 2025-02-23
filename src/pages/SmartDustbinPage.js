import React from 'react';
import './SmartDustbinPage.css'; // Import the CSS file
import { Trash } from 'lucide-react'; // Icon for notifications
import axios from 'axios'; // For API requests

const SmartDustbinPage = () => {
    // Static array for notifications
    const notifications = [
        { id: 1, location: 'TVM', bValue: '70%', nbValue: '20%' },
        { id: 2, location: 'Kowdiar', bValue: '71%', nbValue: '21%' },
        { id: 3, location: 'SS Kovil Road', bValue: '72%', nbValue: '22%' },
        { id: 4, location: 'Vazhuthacaud', bValue: '73%', nbValue: '23%' },
        { id: 5, location: 'Nalanchira', bValue: '74%', nbValue: '24%' },
        { id: 6, location: 'Nedumangad', bValue: '75%', nbValue: '25%' },
        { id: 7, location: 'Parassala', bValue: '76%', nbValue: '26%' },
        { id: 8, location: 'Inchivila', bValue: '77%', nbValue: '27%' },
    ];

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
            console.error("Error fetching report:", error.response || error);
            alert("Failed to fetch report from server.");
        }
    };

    return (
        <div className="smart-dustbin-page">
            <h1>Smart Dustbin Notifications</h1>
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
                            <button
                                className="report-button"
                                onClick={() => handleReport(notification)}
                            >
                                Report
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SmartDustbinPage;
