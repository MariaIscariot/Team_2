import { useState, useEffect } from 'react';
import styles from './index.module.css';
import History from './Subcomponents/History.jsx';
import SendMessage from './Subcomponents/SendMessage.jsx';
import Rezume from './Subcomponents/Rezume.jsx';
import FileProcessor from '../FileProcessor/FileProcessor';

export default function MainBody({ message }) { 
  const [activeAction, setActiveAction] = useState('Send message'); 
  const [sentMessages, setSentMessages] = useState([]);
  const [selectedMessage, setSelectedMessage] = useState(null);


  const renderContent = () => { 
    switch (activeAction) {
      case 'Send message':
        return (
          <>
            <Rezume sentMessages={sentMessages} message={selectedMessage || message} />
            <div className={styles.line}></div>
            <SendMessage message={selectedMessage || message} sentMessages={sentMessages} setSentMessages={setSentMessages}/>
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
      case 'Analyse Document':
        return <FileProcessor />;
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
