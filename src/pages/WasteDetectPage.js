import React, { useState } from 'react';
import './WasteDetectPage.css'; // Import the CSS file for styling

const WasteDetectPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [enlargedImage, setEnlargedImage] = useState(null);

  const images = Array.from({ length: 3 }, (_, i) => require(`../assets/images/image${i + 1}.webp`));

  const filteredImages = images.filter((image, index) =>
    image.toLowerCase().includes(searchTerm.toLowerCase()) || (index + 1).toString().includes(searchTerm)
  );

  return (
    <div className="waste-detect-page">
      <input
        type="text"
        placeholder="Search images..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-bar"
      />
      <div className="image-grid">
        {filteredImages.map((image, index) => (
          <img
            key={index}
            src={image}
            alt={`Waste Detection ${index + 1}`}
            className="image-thumbnail"
            onClick={() => setEnlargedImage(image)}
          />
        ))}
      </div>

      {enlargedImage && (
        <div className="image-overlay" onClick={() => setEnlargedImage(null)}>
          <img src={enlargedImage} alt="Enlarged" className="enlarged-image" />
        </div>
      )}
    </div>
  );
};

export default WasteDetectPage;
