import { useState } from 'react';
import MessageItem from '../../Subjects/Subcomponents/MessageItem.jsx';
import styles from '../index.module.css';

export default function History({ sentMessages }) {
  const [selectedIndex, setSelectedIndex] = useState(null);

  return (
    <div className={styles.historySection}>
      <h3>Istoric Mesaje</h3>
      <div className={styles.messageList}>
        {sentMessages.map((msg, index) => (
          <div key={index}>
            <div
              style={{ cursor: 'pointer' }}
              onClick={() => setSelectedIndex(index)}
            >
              <MessageItem
                sender={msg.sender}
                subject={msg.subject}
                time={msg.time}
                selected={selectedIndex === index}
                onClick={() => setSelectedIndex(index)}
              />
            </div>
            {selectedIndex === index && (
              <div className={styles.messageDescription}>
                <strong>Descriere:</strong> {msg.description}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}