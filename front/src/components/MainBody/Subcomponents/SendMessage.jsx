import { useState } from 'react';
import styles from '../index.module.css';

export default function SendMessage({ message }) {
  const [toField, setToField] = useState('');
  const [ccField, setCcField] = useState('');
  const [messageText, setMessageText] = useState('');
  const [sentMessages, setSentMessages] = useState([]);

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
      setMessageText('');
    }
  };
 
  return (
    <>
        {message && 
        <div className={styles.body}> 
            <h2>{message.subject}</h2>
            <p><strong>From:</strong> {message.sender}</p>
            <p><strong>Time:</strong> {message.time}</p>
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
                <button className={styles.sendButton} onClick={handleSend}>
                Send
                </button>
            </div>
        </div>

        <div className={styles.lastMessage}>
            {message.description}
        </div>
    </div>
    </>
  );
}
