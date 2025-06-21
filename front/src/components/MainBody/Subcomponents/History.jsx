import  { useState } from 'react';
import MessageItem from '../../Subjects/Subcomponents/MessageItem.jsx';
import styles from '../index.module.css';

export default function History({sentMessages}) {
  const [selectedIndex, setSelectedIndex] = useState(null);

  return (
    <div className={styles.historySection}>
      <h3>Istoric Mesage</h3>
      <ul className={styles.messageList}>
        {sentMessages.map((msg, index) => (
          <MessageItem
            key={index}
            sender={msg.sender}
            subject={msg.subject}
            time={msg.time}
            selected={selectedIndex === index}
            onClick={() => setSelectedIndex(index)}
          />
        ))}
      </ul>
    </div>
  );
}