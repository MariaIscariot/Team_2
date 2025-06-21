import styles from './index.module.css';
 
export default function MainBody({ message }) {
  if (!message) {
    return <div className={styles.empty}>Выберите сообщение</div>;
  }

  return (
    <div className={styles.body}>
      <h2>{message.subject}</h2>
      <p><strong>От:</strong> {message.sender}</p>
      <p><strong>Время:</strong> {message.time}</p>
      <p className={styles.content}>
        Здесь будет текст письма или его можно загрузить дополнительно.
      </p>
    </div>
  );
}
