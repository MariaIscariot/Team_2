import styles from '../index.module.css';

export default function Rezume({sentMessages}) {
  return (
    <div className={styles.resumeSection}>
        <h3>Rezumat</h3>
        <p>Total mesaje trimise: {sentMessages.length}</p>
        <p>Ultima activitate: {sentMessages.length > 0 ? sentMessages[sentMessages.length - 1].timestamp : 'N/A'}</p>
    </div>
  );
}