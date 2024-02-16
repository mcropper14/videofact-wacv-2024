// App.js
import React, { useState } from 'react';
import VideoUploader from './VideoUploader';
import ResultsDisplay from './ResultsDisplay';

function App() {
  const [results, setResults] = useState(null);

  const handleResults = (data) => {
    setResults(data);
  };

  return (
    <div className="App">
      <h1>Video Fact</h1>
      <VideoUploader onResults={handleResults} />
      {results && <ResultsDisplay data={results} />}
    </div>
  );
}

export default App;
