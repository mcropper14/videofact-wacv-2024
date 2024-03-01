import React from 'react';

function ResultsDisplay({ data }) {
  return (
    <div>
      <h2>Detection Results</h2>
      <p>Decision: {data.decision}</p>
      <p>First Result: {data.first_result}</p>
      <ul>
        {data.idxs_scores.map((result, index) => (
          <li key={index}>
            Frame Index: {result[0]}, Score: {result[1]}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ResultsDisplay;
