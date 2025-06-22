import { useState, useEffect, useRef } from 'react';
import styles from '../index.module.css';
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa';

export default function SendMessage({ message }) {
  const [messageText, setMessageText] = useState('');
  const [recipients, setRecipients] = useState([]);
  const [attachedFile, setAttachedFile] = useState(null);
  const [approved, setApproved] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (message) {
        setMessageText('Generating response...');
        const requestBody = {
            id: message.id,
            subject: message.subject,
            from: message.sender,
            body: message.description,
        };

        fetch('http://localhost:5000/generate-response', {
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
                    setMessageText(data.output);
                } else {
                    setMessageText('Failed to generate response. The "output" key was not found in the response.');
                }
            })
            .catch((err) => {
                console.error('Error generating response:', err);
                setMessageText(`Error generating response: ${err.message}`);
            });
    } else {
      setMessageText('');
    }
  }, [message]);

  const handleSend = () => {
    if (!message || !messageText) return;

    const formData = new FormData();
    formData.append('sender', message.reciever);
    formData.append('reciever', message.sender);
    formData.append('subject', message.subject);
    formData.append('description', messageText);
    formData.append('time', new Date().toLocaleString());

    if (attachedFile) {
      formData.append('file', attachedFile);
    }

    fetch('http://localhost:5000/api/send', {
      method: 'POST',
      body: formData,
    })
      .then((res) => {
        if (!res.ok) throw new Error('Error');
        return res.json();
      })
      .then((data) => {
        console.log('Sent:', data);
        setMessageText('');
        setAttachedFile(null);
      })
      .catch((err) => {
        console.error('Error:', err);
      });
  };

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setAttachedFile(e.target.files[0]);
    }
  };

  function handleReload(){

    console.log("LEt ger mails!");
    
    fetch('http://localhost:5000/load-emails')
      .then((res) => {
        if (!res.ok) throw new Error('Error');
        return res.json();
      })
      .then((data) => {
        console.log('Sent:', data); 
      })
      .catch((err) => {
        console.error('Error:', err);
      });
  }

  const handleInputChange = (e) => {
    const input = e.target.value;
    const users = input.split(',').map(u => u.trim()).filter(Boolean);
    setRecipients(users);
  };


  return (
    <>
      {message &&
        <div className={styles.body}>
          <div className={styles.something}>
            <h2>{message.subject}</h2>
          </div>
          <div className={styles.messageDetails}>
            <p><strong>From:</strong> {message.sender}</p>
            <p><strong>To:</strong> {message.to}</p>
          </div>
        </div>
      }

      <div className={styles.messageFields}>
        <div className={styles.messageComposer}>
          <div className={styles.messageBody}>
            <textarea
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              rows="10"
            />
          </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <FaThumbsUp
              onClick={() => setApproved('Approved!')}
              style={{ color: 'gray', cursor: 'pointer' }}
            />
            <FaThumbsDown
              onClick={() => setApproved('We will try more!')}
              style={{ color: 'gray', cursor: 'pointer' }}
            />
            {approved == "Approved!" && (<p style={{ color: 'green' }}>{approved}</p>)}
            {approved == "We will try more!" && (<p style={{ color: 'red' }}>{approved}</p>)}
          </div>

          <div className={styles.messageActions}>
            <button className={styles.sendButton} onClick={handleUploadClick} disabled={!message}>
              Upload a file
            </button>
            <button className={styles.sendButton} onClick={handleSend} disabled={!message}>
              Send
            </button>
            <button className={styles.sendButton} onClick={handleReload} disabled={!message}>
              Reload messages
            </button>

            
            <div>
              <strong>Recipients:</strong>
            
            <input
              type="text"
              placeholder="Enter users separated by commas"
              onChange={handleInputChange}
            />
          </div>
          
            </div>

        </div>

        {attachedFile && (
          <div className={styles.attachmentInfo}>
            📎 Прикреплён файл: {attachedFile.name}
          </div>
        )}

        {message &&
          <div className={styles.lastMessage}>
            <div className={styles.something}>
              <h3>Last Message</h3>
              <p>{message.time}</p>
            </div>
            <p><strong>From:</strong> {message.sender}</p>
            <p><strong>To:</strong> {message.to}</p>
            <p><strong>Subject:</strong> {message.subject}</p>
            <div className={styles.line}></div><br />
            {message?.description}
          </div>
        }
      </div>
    </>
  );
}
