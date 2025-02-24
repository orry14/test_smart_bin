import React, { useState, useEffect } from 'react';
import './WasteDetectPage.css'; // Import the CSS file for styling

const WasteDetectPage = () => {
  const [screenshots, setScreenshots] = useState([]);
  const [filteredScreenshots, setFilteredScreenshots] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [enlargedImage, setEnlargedImage] = useState(null);

  // Fetch screenshots from the backend
  useEffect(() => {
    fetch('http://10.10.155.173:5050/api/screenshots')
      .then((response) => response.json())
      .then((data) => {
        setScreenshots(data);
        setFilteredScreenshots(data); // Initially display all screenshots
      })
      .catch((error) => console.error('Error fetching screenshots:', error));
  }, []);

  // Handle search input change
  const handleSearch = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchQuery(query);
    const filtered = screenshots.filter((screenshot) =>
      screenshot.toLowerCase().includes(query)
    );
    setFilteredScreenshots(filtered);
  };

  // Delete Screenshot
  const handleDelete = (screenshot) => {
    const filename = screenshot.split('/').pop(); // Extract filename from path
    fetch(`http://10.10.155.173:5050/api/screenshots/${filename}`, {
      method: 'DELETE',
    })
      .then((response) => {
        if (response.ok) {
          // Remove the deleted screenshot from state
          const updatedScreenshots = screenshots.filter((s) => s !== screenshot);
          setScreenshots(updatedScreenshots);
          setFilteredScreenshots(updatedScreenshots);
        } else {
          console.error('Failed to delete screenshot');
        }
      })
      .catch((error) => console.error('Error deleting screenshot:', error));
  };

  return (
    <div className="waste-detect-page">
      <h1 className="title">Detected Litter Screenshots</h1>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search screenshots..."
        value={searchQuery}
        onChange={handleSearch}
        className="search-bar"
      />

      {/* Display Screenshots with Delete Button */}
      <div className="image-grid">
        {filteredScreenshots.map((screenshot, index) => (
          <div key={index} className="image-wrapper">
            <img
              src={`http://10.10.155.173:5050${screenshot}`}
              alt={`Screenshot ${index + 1}`}
              className="image-thumbnail"
              onClick={() => setEnlargedImage(`http://10.10.155.173:5050${screenshot}`)}
            />
            <button className="delete-button" onClick={() => handleDelete(screenshot)}>Delete</button>
          </div>
        ))}
      </div>

      {/* Enlarged Image View */}
      {enlargedImage && (
        <div className="image-overlay" onClick={() => setEnlargedImage(null)}>
          <img src={enlargedImage} alt="Enlarged" className="enlarged-image" />
        </div>
      )}
    </div>
  );
};

export default WasteDetectPage;
