import React, { useState } from 'react';
import styles from './index.module.css';

export default function MainBody({ message }) {
  const [activeTab, setActiveTab] = useState('Main');
  const [activeAction, setActiveAction] = useState('Send message');
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
      setSentMessages([...sentMessages, newMessage]);
      setToField('');
      setCcField('');
      setMessageText('');
    }
  };

  const renderComposer = () => (
    <div className={styles.messageComposer}>
      <div className={styles.messageFields}>
        
        
      </div>
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
  );

  const renderContent = () => {
    if (message) {
      return (
        <div className={styles.body}>
          <h2>{message.subject}</h2>
          <p><strong>От:</strong> {message.sender}</p>
          <p><strong>Время:</strong> {message.time}</p>
          <p className={styles.content}>
            Здесь будет текст письма или его можно загрузить дополнительно.
          </p>
          {renderComposer()}
        </div>
      );
    }

    switch (activeAction) {
      case 'Send message':
        return renderComposer();

      case 'History':
        return (
          <div className={styles.historySection}>
            <h3>Istoric Mesaje</h3>
            {sentMessages.length === 0 ? (
              <p>Nu există mesaje trimise încă.</p>
            ) : (
              sentMessages.map((msg) => (
                <div key={msg.id} className={styles.messageItem}>
                  <div className={styles.messageHeader}>
                    <strong>To:</strong> {msg.to}
                    {msg.cc && <span> | <strong>CC:</strong> {msg.cc}</span>}
                    <span className={styles.timestamp}>{msg.timestamp}</span>
                  </div>
                  <div className={styles.messageContent}>{msg.text}</div>
                </div>
              ))
            )}
          </div>
        );

      case 'Resume':
        return (
          <div className={styles.resumeSection}>
            <h3>Rezumat</h3>
            <p>Total mesaje trimise: {sentMessages.length}</p>
            <p>Ultima activitate: {sentMessages.length > 0 ? sentMessages[sentMessages.length - 1].timestamp : 'N/A'}</p>
          </div>
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
