import { useState } from 'react';
import styles from './index.module.css';
import History from './Subcomponents/History.jsx';
import SendMessage from './Subcomponents/SendMessage.jsx'
import Rezume from './Subcomponents/Rezume.jsx';

export default function MainBody({ message }) {
  const [activeTab, setActiveTab] = useState('Main');
  const [activeAction, setActiveAction] = useState('Send message'); 
  const [sentMessages, setSentMessages] = useState([]);

  const renderContent = () => {
    switch (activeAction) {
      case 'Send message':
        return <SendMessage message={message}/>
      case 'History':
        return (
          <div className={styles.historySection}>
            <h3>Istoric Mesaje</h3>
            {sentMessages.length === 0 ? (
              <p>Nu există mesaje trimise încă.</p>
            ) : <History sentMessages={sentMessages} />}
          </div>
        );
      case 'Resume':
        return (
          <Rezume sentMessages={sentMessages}/>
        );

      default:
        return <div className={styles.empty}>Selectează o acțiune</div>;
    }
  };

  return (
    <div className={styles.mainBodyOutlook}>
      <aside className={styles.sidebar}>
        <nav className={styles.mainNavbar}>
          {['Main', 'HR', 'Instagram'].map((tab) => (
            <button
              key={tab}
              className={`${styles.navTab} ${activeTab === tab ? styles.active : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </nav>

        <div className={styles.actionButtons}>
          {['Send message', 'History', 'Resume'].map((action) => (
            <button
              key={action}
              className={`${styles.actionBtn} ${activeAction === action ? styles.active : ''}`}
              onClick={() => setActiveAction(action)}
            >
              {action}
            </button>
          ))}
        </div>
      </aside>

      <main className={styles.mainContent}>
        <div className={styles.contentHeader}>
          <h2>{activeTab} - {activeAction}</h2>
        </div>
        <div className={styles.contentBody}>
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
