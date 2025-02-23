import React from 'react';
import './HomePage.css'; // Import CSS for HomePage styling

const HomePage = () => {
  return (
    <div className="home-page">
      <video className="home-video" controls autoPlay loop muted>
        <source src="/video.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default HomePage;
