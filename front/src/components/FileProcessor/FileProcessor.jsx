import React, { useState } from 'react';
import styles from './index.module.css';

const FileProcessor = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [analysisData, setAnalysisData] = useState(null);
  const [finalAnalysis, setFinalAnalysis] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setAnalysisResult(null);
      setError('');
      setFinalAnalysis(null);
      handleFileUpload(file);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setProcessing(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/process-file', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnalysisResult(`File processed successfully. Type: ${data.type}, Summary: ${data.summary}`);
      setAnalysisData(data);
    } catch (e) {
      console.error('Error processing file:', e);
      setError('Error processing file. Please check the console for details.');
      setAnalysisResult(null);
    } finally {
      setProcessing(false);
    }
  };

  const handleAnalyze = async () => {
    if (!analysisData) {
      setError('No analysis data available. Please process a file first.');
      return;
    }

    setAnalyzing(true);
    setError('');
    setFinalAnalysis(null);

    try {
      const response = await fetch('http://localhost:5000/analyze-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(analysisData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setFinalAnalysis(result);

    } catch (e) {
      console.error('Error analyzing data:', e);
      setError('Error analyzing data. Please check the console for details.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className={styles.fileProcessor}>
      <h2>File Analysis</h2>
      <div className={styles.controls}>
        <label htmlFor="file-upload" className={styles.customFileUpload}>
          Choose File
        </label>
        <input id="file-upload" type="file" onChange={handleFileChange} style={{ display: 'none' }} />
        {selectedFile && <span className={styles.fileName}>{selectedFile.name}</span>}
        <button onClick={handleAnalyze} disabled={!analysisData || analyzing}>
          {analyzing ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
      {processing && <p>Processing file...</p>}
      {error && <p className={styles.error}>{error}</p>}
      {analysisResult && <p className={styles.result}>{analysisResult}</p>}
      {finalAnalysis && (
        <div className={styles.analysisOutput}>
          <h3>Analysis Result</h3>
          <pre>{finalAnalysis.output}</pre>
        </div>
      )}
    </div>
  );
};

export default FileProcessor; 