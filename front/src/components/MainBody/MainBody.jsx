import { useState, useEffect } from 'react';
import styles from './index.module.css';
import History from './Subcomponents/History.jsx';
import SendMessage from './Subcomponents/SendMessage.jsx';
import Rezume from './Subcomponents/Rezume.jsx';

export default function MainBody({ message }) { 
  const [activeAction, setActiveAction] = useState('Send message'); 
  const [sentMessages, setSentMessages] = useState([]);

  useEffect(() => {
    console.log('Fetching data from backend...');
    fetch('http://localhost:5000/get-subjects')
      .then((res) => {
        console.log('Response status:', res.status);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log('Received data:', data);
        if (data.messages && Array.isArray(data.messages)) {
          setSentMessages(data.messages);
          console.log('Messages set successfully:', data.messages.length, 'messages');
        } else {
          console.error('Invalid data structure:', data);
          throw new Error('Invalid data structure received');
        }
      })
      .catch((err) => {
        console.error('Fetch error:', err);
        setSentMessages([]);
      });
  }, []);

  const renderContent = () => { 
    switch (activeAction) {
      case 'Send message':
        return (
          <>
            <Rezume sentMessages={sentMessages} />
            <div className={styles.line}></div>
            <SendMessage message={message} sentMessages={sentMessages} setSentMessages={setSentMessages}/>
          </>
        );
      case 'History':
        return (
          <div className={styles.historySection}>
            {sentMessages.length === 0 ? (
              <p>There are no messages in this conversation.</p>
            ) : (
              <History sentMessages={sentMessages} />
            )}
          </div>
        );
      default:
        return <></>;
    }  
  };

  return (
    <div className={styles.mainBodyOutlook}>
      <aside className={styles.sidebar}> 
        <div className={styles.actionButtons}>
          {['Send message', 'History', 'Analyse Document'].map((action) => (
            <button
              key={action}
              className={`${styles.actionBtn} ${activeAction === action ? styles.active : ''}`}
              onClick={() => setActiveAction(action)}
            >  {action} </button>
          ))}
        </div> 
      </aside>

      <main className={styles.mainContent}>
        <div className={styles.contentHeader}>
          <h2>{activeAction}</h2>
        </div>
        <div className={styles.contentBody}>
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
