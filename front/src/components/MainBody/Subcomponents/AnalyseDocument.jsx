import styles from '../index.module.css';
import React, { useState } from 'react';

const parseAnalysis = (text) => {
    if (!text) return null;

    try {
        const getSection = (start, end) => {
            const startIndex = text.indexOf(start);
            if (startIndex === -1) return '';
            const endIndex = end ? text.indexOf(end, startIndex) : text.length;
            return text.substring(startIndex + start.length, endIndex).trim();
        };

        const topic = getSection('Topic:', 'Key Points:');
        const keyPointsText = getSection('Key Points:', 'Conclusion:');
        const conclusion = getSection('Conclusion:', 'Relevant Quotes (if applicable):');
        const quotesText = getSection('Relevant Quotes (if applicable):');

        const keyPoints = keyPointsText.split('*').map(p => p.trim()).filter(Boolean);
        const quotes = quotesText.split('*').map(q => q.trim().replace(/"/g, '')).filter(Boolean);

        if (!topic) {
             return { raw: text };
        }

        return { topic, keyPoints, conclusion, quotes };
    } catch (e) {
        console.error("Failed to parse analysis:", e);
        return { raw: text };
    }
};


export default function AnalyseDocument() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setAnalysisResult(null);
    setError('');
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    setIsLoading(true);
    setError('');
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Step 1: Process the file
      const processResponse = await fetch('http://localhost:5000/process-file', {
        method: 'POST',
        body: formData,
      });

      if (!processResponse.ok) {
        const errorData = await processResponse.json();
        throw new Error(errorData.stderr || errorData.error || `Process file error! status: ${processResponse.status}`);
      }

      const processData = await processResponse.json();

      // Step 2: Analyze the JSON output from the first step
      const analyzeResponse = await fetch('http://localhost:5000/analyze-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processData.results),
      });

      if (!analyzeResponse.ok) {
        const errorData = await analyzeResponse.json();
        throw new Error(errorData.stderr || errorData.error || `Analyze JSON error! status: ${analyzeResponse.status}`);
      }

      const analyzeData = await analyzeResponse.json();
      setAnalysisResult(parseAnalysis(analyzeData.output));

    } catch (err) {
      console.error('Error during file analysis:', err);
      setError(err.message || 'Failed to analyze the document. Please check the console for more details.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.resumeSection}>
      <h2>Analyse Document</h2>
      <p>Select a document (PDF, DOCX, TXT, XLSX) to analyze.</p>
      
      <div className={styles.fileUploadContainer}>
        <label htmlFor="file-upload" className={styles.customFileUpload}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style={{flexShrink: 0}}>
                <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
            </svg>
            <span>Choose File</span>
        </label>
        <input id="file-upload" type="file" onChange={handleFileChange} accept=".pdf,.docx,.txt,.xlsx" />
        {selectedFile && <span className={styles.fileName}>{selectedFile.name}</span>}
        <button onClick={handleFileUpload} disabled={isLoading || !selectedFile} className={styles.analyzeButton}>
          {isLoading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {error && <p className={styles.error}>{error}</p>}

      {analysisResult && (
        <div className={styles.analysisResult}>
            {analysisResult.raw ? (
                <pre>{analysisResult.raw}</pre>
            ) : (
                <>
                    <h3 className={styles.analysisTopic}>{analysisResult.topic}</h3>
                    
                    <h4 className={styles.analysisSectionTitle}>Key Points</h4>
                    <ul>
                        {analysisResult.keyPoints.map((point, index) => <li key={index}>{point}</li>)}
                    </ul>

                    <h4 className={styles.analysisSectionTitle}>Conclusion</h4>
                    <p>{analysisResult.conclusion}</p>

                    {analysisResult.quotes && analysisResult.quotes.length > 0 && (
                        <>
                            <h4 className={styles.analysisSectionTitle}>Relevant Quotes</h4>
                            {analysisResult.quotes.map((quote, index) => <blockquote key={index}>{quote}</blockquote>)}
                        </>
                    )}
                </>
            )}
        </div>
      )}
    </div>
  );
} 