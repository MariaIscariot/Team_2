import React, { useState, useEffect } from 'react';
import MessageItem from '../Subjects/Subcomponents/MessageItem.jsx';
import styles from './index.module.css';

const FileProcessor = () => {
  const [messages, setMessages] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch('http://localhost:5000/get-subjects');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      // Filter messages that have attachments
      const messagesWithAttachments = data.messages.filter(
        (msg) => msg.attachments && msg.attachments.length > 0
      );
      
      setMessages(messagesWithAttachments);
    } catch (err) {
      console.error('Error fetching messages:', err);
      setError('Error fetching messages. Please check the console for details.');
    }
  };

  const handleItemClick = async (index) => {
    if (selectedIndex === index) {
      setSelectedIndex(null);
      setAnalysisResult(null);
    } else {
      setSelectedIndex(index);
      const clickedMessage = messages[index];
      
      // Process the first attachment
      if (clickedMessage.attachments && clickedMessage.attachments.length > 0) {
        await processAttachment(clickedMessage.attachments[0]);
      }
    }
  };

  const processAttachment = async (attachment) => {
    setProcessing(true);
    setError('');
    setAnalysisResult(null);

    try {
      // Step 1: Process the file by path
      const processRequestBody = {
        filepath: attachment.filepath
      };

      const processResponse = await fetch('http://localhost:5000/process-file-by-path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processRequestBody),
      });

      if (!processResponse.ok) {
        throw new Error(`HTTP error! status: ${processResponse.status}`);
      }

      const processData = await processResponse.json();
      
      // Step 2: Analyze the processed data
      const analyzeResponse = await fetch('http://localhost:5000/analyze-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processData.results || processData),
      });

      if (!analyzeResponse.ok) {
        throw new Error(`HTTP error! status: ${analyzeResponse.status}`);
      }

      const analyzeData = await analyzeResponse.json();
      setAnalysisResult(analyzeData);
    } catch (e) {
      console.error('Error processing attachment:', e);
      setError('Error processing attachment. Please check the console for details.');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className={styles.fileProcessor}>
      <h2>Files with Attachments</h2>
      {error && <p className={styles.error}>{error}</p>}
      
      <div className={styles.messageList}>
        {messages.length === 0 ? (
          <p>No messages with attachments found.</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index}>
              <div
                style={{ cursor: 'pointer' }}
                onClick={() => handleItemClick(index)}
              >
                <MessageItem
                  sender={msg.sender}
                  subject={msg.subject}
                  time={msg.time}
                  selected={selectedIndex === index}
                />
              </div>
              {selectedIndex === index && (
                <div className={styles.messageDescription}>
                  <strong>Attachments:</strong> {msg.attachments_count} file(s)
                  {msg.attachments && msg.attachments.map((attachment, idx) => (
                    <div key={idx} className={styles.attachmentInfo}>
                      📎 {attachment.filename} ({attachment.content_type})
                    </div>
                  ))}
                  {processing && <p>Processing attachment...</p>}
                  {analysisResult && (
                    <div className={styles.analysisOutput}>
                      <h3>Analysis Result</h3>
                      {analysisResult.output ? (
                        <pre>{analysisResult.output}</pre>
                      ) : (
                        <pre>{JSON.stringify(analysisResult, null, 2)}</pre>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default FileProcessor; 