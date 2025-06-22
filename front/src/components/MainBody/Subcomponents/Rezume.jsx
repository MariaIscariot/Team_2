import styles from '../index.module.css';
import React, { useEffect, useState } from 'react';

export default function Rezume({sentMessages, message}) {

  const [summary, setSummary] = useState('');

  useEffect(() => {
    if (message) {
      setSummary('Loading summary...');
      const requestBody = {
        id: message.id,
        subject: message.subject,
        from: message.sender,
        body: message.description,
      };

      fetch('http://localhost:5000/summarize-conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      })
        .then((res) => {
          if (!res.ok) {
              throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        }) 
        .then((data) => {
          if (data.output) {
            setSummary(data.output)
          } else {
            setSummary('Failed to load summary. The "output" key was not found in the response.');
          }
        })
        .catch((err) => {
          console.error('Error while getting summary:', err);
          setSummary('Error loading data.');
        });
    } else {
      setSummary('Select a message to see the summary.');
    }
  }, [message]);
    
  return (
    <div className={styles.resumeSection}>
        <h2>Summary</h2>
        <p> {summary} </p>
        <p>All sent messages: {sentMessages?.length || 0}</p>
        <p>Last activity: {sentMessages?.length > 0 ? sentMessages[sentMessages?.length - 1].time : 'Not enough information'}</p>
    </div>
  );
}