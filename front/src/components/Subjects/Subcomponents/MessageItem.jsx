import styles from '../index.module.css';

export default function MessageItem({ sender, subject, time, selected, onClick, seen }) {
  return (
    <li
      className={`${styles.item} 
                  ${selected ? styles.selected : ''} 
                  ${!seen ? styles.unread : ''}`}
      onClick={onClick}
    >
      <div className={styles.sender}>{sender}</div>
      <div className={styles.subject}>{subject}</div>
      <div className={styles.time}>{time}</div>
    </li>
  );
}
