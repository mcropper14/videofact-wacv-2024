import React, { useState } from 'react';

function VideoUploader({ onResults }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false); // State to track loading progress

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    console.log('Submitting form...');
    if (!selectedFile) {
      console.error('No file selected.');
      return;
    }

    setLoading(true); // Set loading to true when analysis starts

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/analyze-video', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      //setResults(data);
      onResults(data);
    } catch (error) {
      console.error('Error analyzing video:', error);
    } finally {
      setLoading(false); // Set loading to false when analysis is complete
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Video'}
      </button>
    </div>
  );
}

export default VideoUploader;

