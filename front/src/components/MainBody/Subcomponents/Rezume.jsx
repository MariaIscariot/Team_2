import styles from '../index.module.css';
import React, { useEffect, useState } from 'react';

export default function Rezume({sentMessages}) {

  const [summary, setSummary] = useState('');

  useEffect(() => {
    fetch('http://localhost:3000/api/summary')
      .then((res) => res.text()) 
      .then((data) => setSummary(data))
      .catch((err) => {
        console.error('Error while getting summary:', err);
        setSummary('Error loading data.');
      });
  }, []);
    
  return (
    <div className={styles.resumeSection}>
        <h2>Summary</h2>
        <p> {summary} </p>
        <p>All sent messages: {sentMessages?.length || 0}</p>
        <p>Last activity: {sentMessages?.length > 0 ? sentMessages[sentMessages?.length - 1].time : 'Not enough information'}</p>
    </div>
  );
}