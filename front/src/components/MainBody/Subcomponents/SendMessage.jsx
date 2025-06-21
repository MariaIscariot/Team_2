import { useState } from 'react';
import styles from '../index.module.css';

export default function SendMessage({ message }) {
  const [toField, setToField] = useState('');
  const [ccField, setCcField] = useState('');
  const [messageText, setMessageText] = useState('');  

  const handleSend = () => {
    if (toField && messageText) {
      const newMessage = {
        id: Date.now(),
        to: toField,
        cc: ccField,
        text: messageText,
        timestamp: new Date().toLocaleString(),
      };
      setSentMessages((prev) => [...prev, newMessage]);
      setToField('');
      setCcField(''); 
    }
  };
 
  return (
    <>
        {message && 
        <div className={styles.body}> 
            <div className={styles.something}>
                <h2>{message.subject}</h2> 
            </div>
            <p><strong>From:</strong> {message.reciever}</p>
            <p><strong>To:</strong> {message.sender}</p>
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
            <div className={styles.messageActions}>
                <button className={styles.editButton} onClick={handleSend}>
                Edit
                </button>
                <button className={styles.uploadButton} onClick={handleSend}>
                Upload a file
                </button>
                <button className={styles.sendButton} onClick={handleSend}>
                Send
                </button>
            </div>
        </div>

        {message && 

        <div className={styles.lastMessage}>

            <div className={styles.something}>
                <h3>Last Message</h3> 
                <p>{message.time}</p>
            </div>
            <p><strong>From:</strong> {message.sender}</p>
            <p><strong>To:</strong> {message.reciever}</p>
            <p><strong>Subject:</strong> {message.subject}</p>
            <div className={styles.line}></div><br/>
            {message?.description}
        </div>
        }
    </div>
    </>
  );
}
