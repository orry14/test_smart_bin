import React from 'react';
import './HomePage.css'; // Import CSS for HomePage styling

const HomePage = () => {
  return (
    <div className="home-page">
      <h1 className="title">Live CCTV Feed - Litter Detection</h1>
      <div className="video-container">
        <img
          src="http://10.10.155.173:5050/video_feed"
          alt="Live CCTV Feed"
          className="live-video"
        />
      </div>
    </div>
  );
};

export default HomePage;
